def decideActivityType(activityType: str) -> int:
    """
    2：签到
    4：抢答
    5：主题讨论
    14：问卷
    35：分组任务
    42：随堂练习
    43：投票
    45：通知
    """
    if activityType == "signin":
        return 2
    elif activityType == "quiz":
        return 42
    else:
        return None