from multiprocessing import Pool, set_start_method

if __name__ == "__main__":
    import email.header
    import email_utils
    import sys
    from config import config
    from console import console, print_result

    console.print("ImapXT (By XiaoDeng3386)")

    set_start_method("spawn")
    if not email_utils.test_server():
        sys.exit(1)
    pool = Pool()
    results = []
    for email_conf in config.emails:
        results.append((email_conf.user, pool.apply_async(email_utils.fetch, args=(email_conf,))))
    pool.close()
    pool.join()

    console.log("执行完成，正在合并数据 ...")
    email_list = []
    for address, result in results:
        for e in result.get():
            email_list.append((
                address,
                email.header.decode_header(e["Subject"])[0][0].decode()
            ))
    console.log(f"成功获取到 {len(email_list)} 个结果")
    print_result(email_list)


