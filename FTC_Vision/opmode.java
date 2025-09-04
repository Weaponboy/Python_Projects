@TeleOp(name="Pookie Texpand Testing", group="Debugging")
@Config
public class VisionGrabPookieTexpand extends LinearOpMode {

    // LL PIPELINE INDEXES:
    // 5 is RED

    private RH robot = RH.getInstance();
    private GamepadEx gamepadEx1;
    private GamepadEx gamepadEx2;

    private double clawOffsetFromSlides = 5.19685;
    private double angle;

    public Vector2D targetPosition = new Vector2D(clawOffsetFromSlides, clawOffsetFromSlides);

    @Override
    public void runOpMode() throws InterruptedException {
        gamepadEx1 = new GamepadEx(gamepad1);
        gamepadEx2 = new GamepadEx(gamepad2);

        robot.init(hardwareMap, telemetry, true);
        robot.limelight.pipelineSwitch(5);
        robot.limelight.deleteSnapshots();
        robot.detectorResults = null;

        robot.ll.switchPipeline(5);
        robot.ll.collectColoredSamples(true);
        robot.ll.setDetectionColor(true);
        robot.ll.setTargetColor(Limelight.DetectionColour.RED);
        robot.ll.setAuto(true);

        Globals.alliance = Globals.Alliance.RED;

        robot.intake.updateTurret(IntakeSubsystem.TurretState.VISION_SCANNING);
        robot.intake.updateArm(IntakeSubsystem.ArmState.AIM);
        robot.intake.write();

        CommandScheduler.getInstance().reset();

        gamepadEx1.getGamepadButton(GamepadKeys.Button.DPAD_UP)
                .whenPressed(
                        new SequentialCommandGroup(
                                new IntakeTurretCommand(IntakeSubsystem.TurretState.VISION_SCANNING),
                                new IntakeArmCommand(IntakeSubsystem.ArmState.AIM),
                                new WaitCommand(150),
                                new SequentialCommandGroup(
                                        new InstantCommand(this::target),
                                        new WaitUntilCommand(() -> RH.getInstance().intakeSlideActuator.hasReached()).withTimeout(800),
                                        new WaitCommand(50),
                                        new InstantCommand(() -> Globals.READ_INTAKE_COLOR = true),
                                        new InstantCommand(() -> Globals.GOT_6TH_SAMPLE_SPEC = true)
                                )
                        )
                );

        gamepadEx1.getGamepadButton(GamepadKeys.Button.DPAD_DOWN)
                        .whenPressed(
                                new SequentialCommandGroup(
                                        new IntakeTurretCommand(IntakeSubsystem.TurretState.VISION_SCANNING),
                                        new IntakeArmCommand(IntakeSubsystem.ArmState.AIM),
                                        new IntakeHorizontalCommand(-1),
                                        new IntakeClawCommand(IntakeSubsystem.ClawState.OPEN)
                                )
                        );

        gamepadEx1.getGamepadButton(GamepadKeys.Button.DPAD_RIGHT)
                        .whenPressed(
                                new SequentialCommandGroup(
                                        new IntakeDownCommand()
                                )
                        );

        gamepadEx1.getGamepadButton(GamepadKeys.Button.Y)
                        .whenPressed(new DeliveryVerticalCommand(670));
        gamepadEx1.getGamepadButton(GamepadKeys.Button.B)
                        .whenPressed(new DeliveryVerticalCommand(-1));

        telemetry.addData("LL RUN", robot.limelight.isRunning());
        telemetry.addData("LL CXN", robot.limelight.isConnected());
        telemetry.addData("LL IDX", robot.limelight.getStatus().getPipelineIndex());
        telemetry.update();

        waitForStart();
        robot.ll.start();

        robot.ll.setReturningData(true);
        robot.ll.setGettingResults(true);

        while (opModeIsActive() && !isStopRequested()) {
            CommandScheduler.getInstance().run();
            robot.clearBulkCache();
            robot.read();
            robot.periodic();
            robot.write();

            robot.ll.execute();
            robot.ll.updatePython(robot.delivery.getSlidePositionCM());

            if (robot.ll.readTarget() != null) {
                TargetSample t = robot.ll.readTarget();
                targetPosition = t.getTargetPoint();
                angle = t.getAngle();

                telemetry.addData("target x", targetPosition.getX());
                telemetry.addData("target y", targetPosition.getY());
                telemetry.addData("target angle", angle);
            } else telemetry.addLine("nothing detected you fucking dumbass");

            telemetry.addData("slide height CM", robot.delivery.getSlidePositionCM());

            telemetry.update();
        }
    }

    public void target() {
        double[] res = inverseKinematics();
        target(res);
    }

    public void target(double[] res) {
        RH robot = RH.getInstance();
        telemetry.addData("res 0", res[0]);
        telemetry.addData("res 1", res[1]);
        telemetry.addData("res 2", res[2]);
        robot.intake.updateArm(IntakeSubsystem.ArmState.AIM);
        robot.intake.updateClaw(IntakeSubsystem.ClawState.FULL_OPEN);
        robot.intakeWristActuator.setTargetPosition(res[2]);
        robot.intakeSlideActuator.setTargetPosition(res[0]);
        robot.intakeTurretActuator.setTargetPosition(res[1]);
    }

    public double[] inverseKinematics() {
        if (robot.ll.readTarget() != null) {
            TargetSample t = robot.ll.commitTarget();

            double forwardCM = targetPosition.getX();
            double sideInches = -targetPosition.getY() / 2.54;
            double estimatedAngle = t.getAngle();

            if (estimatedAngle > 50) estimatedAngle = 90; // og 90
            else estimatedAngle = 0; // og 0

            double forwardInches = forwardCM / 2.54 - 1.3; // tune constant?

            if (Math.abs(sideInches) < armLength) {

                telemetry.addLine("SAMPLE ABLE TO BE GRABBED!");

                double a, b = sideInches, c = armLength;
                double turretTurnAngle = (Math.signum(b) * Math.toDegrees(Math.asin(Math.abs(b) / c)));

                a = Math.sqrt(Math.pow(c, 2) - Math.pow(b, 2));

                double intakeHorizontalInches = forwardInches - a;

                double intakeHorizontalTicks = (int) (intakeHorizontalInches * encoderTicksPerInch);

                double turretTicks = turretTurnAngle * servoTicksPerDegree + RH.getInstance().intake.getTurretStatePosition(IntakeSubsystem.TurretState.CENTER);
                
                double wristAngle = estimatedAngle - turretTurnAngle;
                
                if (wristAngle >= 90) wristAngle -= 180;
                else if (wristAngle <= -90) wristAngle += 180;

                // 0.5 is mid (grippers vertical)
                double wristTicks = 0.5 - wristAngle * spinTicksPerDegree;

                turretTicks = MathUtils.clamp(turretTicks, 0.25, 0.7); // prevent turret from tweaking

                telemetry.addData("intake inches", intakeHorizontalInches);
                telemetry.addData("intake ticks", intakeHorizontalTicks);
                telemetry.addData("sample orientation", estimatedAngle);
                telemetry.addData("turret angle", turretTurnAngle);
                telemetry.addData("wrist angle", wristAngle);
                telemetry.addData("wrist ticks", wristTicks);
                telemetry.addLine("=================================");
                return new double[] {intakeHorizontalTicks, turretTicks, wristTicks};
            }

            telemetry.addData("Estimated Angle", estimatedAngle);
            telemetry.addData("Forward", forwardCM);
            telemetry.addData("Side", sideInches);
        }
        //return new double[] {-26000, -26000, -26000}; // hehe
        return new double[] {0, 0, 0};
    }
}