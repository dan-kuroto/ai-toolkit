import argparse

from plyer import notification


def main():
    parser = argparse.ArgumentParser(description="发送系统桌面通知")
    parser.add_argument("--title", "-t", required=True, help="通知标题")
    parser.add_argument("--message", "-m", required=True, help="通知内容")
    args = parser.parse_args()

    notification.notify(title=args.title, message=args.message)


if __name__ == "__main__":
    main()
