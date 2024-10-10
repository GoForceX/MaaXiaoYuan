from maa.toolkit import Toolkit
from maa.context import Context
from maa.custom_action import CustomAction
from maa.custom_recognition import CustomRecognition


def main():
    # 注册自定义动作
    Toolkit.pi_register_custom_action("Swipe", Swipe())

    Toolkit.pi_register_custom_recognition("RecogNumber", RecogNumber())

    # 启动 MaaPiCli
    Toolkit.pi_run_cli("./assets", "./assets", False)


class RecogNumber(CustomRecognition):
    def analyze(
        self, context: Context, argv: CustomRecognition.AnalyzeArg
    ) -> CustomRecognition.AnalyzeResult:
        print(f"on RecogNumber.run, context: {context}, argv: {argv}")
        image = context.tasker.controller.cached_image
        left_recog = context.run_recognition(
            "OCR", image, {"OCR": {"recognition": "OCR", "roi": [261, 275, 75, 100]}}
        )
        right_recog = context.run_recognition(
            "OCR", image, {"OCR": {"recognition": "OCR", "roi": [401, 288, 75, 100]}}
        )
        print(left_recog.best_result.text)
        print(right_recog.best_result.text)
        return CustomRecognition.AnalyzeResult(
            box=left_recog.box,
            detail=left_recog.best_result.text + "/" + right_recog.best_result.text,
        )


class Swipe(CustomAction):
    def run(
        self, context: Context, argv: CustomAction.RunArg
    ) -> CustomAction.RunResult:

        print(f"on Swipe.run, context: {context}, argv: {argv}")
        left, right = argv.reco_detail.best_result.detail.split("/")
        print(left, right)

        if left > right:
            context.tasker.controller.post_swipe(100, 100, 200, 200, 50).wait()
            context.tasker.controller.post_swipe(200, 200, 100, 300, 50).wait()

        elif left < right:
            context.tasker.controller.post_swipe(200, 100, 100, 200, 50).wait()
            context.tasker.controller.post_swipe(100, 200, 200, 300, 50).wait()
        else:
            context.tasker.controller.post_swipe(100, 100, 200, 100, 50).wait()
            context.tasker.controller.post_swipe(100, 200, 200, 200, 50).wait()

        context.override_next(argv.current_task_name, ["WaitUntilStable"])
        return CustomAction.RunResult(success=True)


if __name__ == "__main__":
    main()
