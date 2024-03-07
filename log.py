async def start(thread):
    logger.info(f"Поток {thread} | Начал работу")
    while True:
        act = await random_line('data/private_keys.txt')
        if not act: break

        if '::' in act:
            private_key, proxy = act.split('::')
        else:
            private_key = act
            proxy = None

        starry = StarryNift(key=private_key, referral_link=config.REF_LINK, bnb_rpc=config.BNB_RPC, proxy=proxy)
        if await starry.login():
            if not await starry.check_minted_pass():
                await starry.mint_pass(logger=logger, thread=thread, gas_price=config.MINT_GWEI)

            time_to_claim = await starry.get_daily_claim_time()
            if time_to_claim == 0:
                await starry.daily_claim(logger, thread, config.MINT_GWEI)
            else: logger.warning(f"Поток {thread} | Следующий клейм через {str(timedelta(seconds=time_to_claim))}: {starry.web3_utils.acct.address}")

        await starry.logout()
    logger.info(f"Поток {thread} | Закончил работу")
