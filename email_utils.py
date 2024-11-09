from config import config, EmailConfig
from console import console
from cache import get_read_emails, add_read_emails
from imaplib import IMAP4, IMAP4_SSL
import email

IMAP_CLIENT = IMAP4_SSL | IMAP4

def get_client() -> IMAP_CLIENT:
    if config.ssl:
        return IMAP4_SSL(config.server)
    else:
        return IMAP4(config.server)

def test_server() -> bool:
    with get_client() as server:
        resp = server.noop()
        console.log(f"服务器 NOOP 回复: {resp}")
    return resp[0] == "OK"

def get_unread_emails(client: IMAP_CLIENT, address: str) -> list[str]:
    stat, data = client.search(None, "ALL")
    if stat != "OK":
        console.log(f"({address}) 搜索邮件时出现错误: {stat} {data}")
        raise SystemError
    email_list = data[0].decode().split(" ")
    read_emails = get_read_emails(address)
    return [e for e in email_list if e not in read_emails]

def fetch_email(client: IMAP_CLIENT, num: str, address: str) -> email.message.Message:
    stat, data = client.fetch(num, "(RFC822)")
    if stat != "OK" or data[0] is None:
        console.log(f"({address}) 拉取邮件({num})时出现错误: {stat} {data}")
        raise SystemError
    add_read_emails(address, num)
    return email.message_from_bytes(data[0][1])

def fetch(email_conf: EmailConfig) -> list[email.message.Message]:
    emails = []
    address = email_conf.user[:]
    with get_client() as client:
        if (r := client.login(email_conf.user, email_conf.password))[0] != "OK":
            console.log(f"({address}) 登录失败: {r}")
            raise SystemError
        client.select()
        for n in get_unread_emails(client, address):
            emails.append(fetch_email(client, n, address))
    console.log(f"({address}) 拉取完成！（未读: {len(emails)}）")
    return emails



