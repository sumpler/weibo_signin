import json
import requests
import random
import time
from urllib.parse import urlparse, parse_qs
import os
import logging
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('weibo_signin.log')
    ]
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

SIGN_URL = "https://api.weibo.cn/2/page/button"
BARK_SERVER = os.getenv('BARK_SERVER', 'https://api.day.app')  # 设置默认值
BARK_KEY = os.getenv('BARK_KEY')  # 全局 Bark Key

# 加载账号配置
try:
    weibo_accounts_str = os.getenv('WEIBO_ACCOUNTS')
    if not weibo_accounts_str:
        raise ValueError("请在 .env 文件中设置 WEIBO_ACCOUNTS 环境变量")
    
    # 移除可能存在的单引号或双引号
    print(f"weibo_accounts_str: {weibo_accounts_str}")
    WEIBO_ACCOUNTS = json.loads(weibo_accounts_str)
    
    if not isinstance(WEIBO_ACCOUNTS, list):
        raise ValueError("WEIBO_ACCOUNTS 必须是一个数组")
    
    if not WEIBO_ACCOUNTS:
        raise ValueError("WEIBO_ACCOUNTS 不能为空数组")
        
    # 验证每个账号的必要字段
    for account in WEIBO_ACCOUNTS:
        if not isinstance(account, dict):
            raise ValueError("WEIBO_ACCOUNTS 中的每个项目必须是一个对象")
        if 'name' not in account:
            raise ValueError("每个账号必须包含 name 字段")
        if 'card_list_cookie_url' not in account:
            raise ValueError("每个账号必须包含 card_list_cookie_url 字段")
            
except json.JSONDecodeError as e:
    raise ValueError(f"WEIBO_ACCOUNTS 环境变量格式错误，请确保是有效的 JSON 格式: {str(e)}")
except Exception as e:
    raise ValueError(f"配置错误: {str(e)}")

if not BARK_KEY:
    logger.warning("未配置 BARK_KEY，将不会发送通知")

def send_request(url, params, headers):
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return None
    return None

def extract_params(url):
    parsed_url = urlparse(url)
    params_from_url = parse_qs(parsed_url.query)
    params_from_url = {k: v[0] for k, v in params_from_url.items()}
    return params_from_url

def get_card_type_11(params, headers, since_id):
    params['since_id'] = since_id
    response = requests.request("GET", params['card_list_cookie_url'], headers=headers, data={})
    data = response.json()
    if data is None:
        return []
    cards = data.get("cards", [])
    card_type_11_info = []
    for card in cards:
        card_group = card.get("card_group", [])
        for item in card_group:
            if item.get("card_type") == '8':
                info = {
                    "scheme": item.get("scheme"),
                    "title_sub": item.get("title_sub"),
                    "signin_status": False if item["buttons"][0]["name"]=="签到" else True
                }
                card_type_11_info.append(info)
    return card_type_11_info

def sign_in(headers, base_params, scheme, since_id):
    params = extract_params(scheme)
    request_url = f"http://i.huati.weibo.com/mobile/super/active_fcheckin?cardid=bottom_one_checkin&container_id={params['containerid']}&pageid={params['containerid']}&scheme_type=1"
    sign_in_params = {
        "aid": base_params.get("aid"),
        "b": base_params.get("b"),
        "c": base_params.get("c"),
        "from": base_params.get("from"),
        "ft": base_params.get("ft"),
        "gsid": base_params.get("gsid"),
        "lang": base_params.get("lang"),
        "launchid": base_params.get("launchid"),
        "networktype": base_params.get("networktype"),
        "s": base_params.get("s"),
        "sflag": base_params.get("sflag"),
        "skin": base_params.get("skin"),
        "ua": base_params.get("ua"),
        "v_f": base_params.get("v_f"),
        "v_p": base_params.get("v_p"),
        "wm": base_params.get("wm"),
        "fid": "232478_-_one_checkin",
        "lfid": base_params.get("lfid"),
        "luicode": base_params.get("luicode"),
        "moduleID": base_params.get("moduleID"),
        "orifid": base_params.get("orifid"),
        "oriuicode": base_params.get("oriuicode"),
        "request_url": request_url,
        "since_id": since_id,
        "source_code": base_params.get("source_code"),
        "sourcetype": "page",
        "uicode": base_params.get("uicode"),
        "ul_sid": base_params.get("ul_sid"),
        "ul_hid": base_params.get("ul_hid"),
        "ul_ctime": base_params.get("ul_ctime"),
    }
    data = send_request(SIGN_URL, sign_in_params, headers)
    return data

def send_bark(title, content):
    if not BARK_KEY:
        return
    
    url = f"{BARK_SERVER}/{BARK_KEY}/{title}/{content}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Bark 通知发送失败: {response.status_code}")
    except Exception as e:
        logger.error(f"Bark 通知发送异常: {str(e)}")

def process_account(account):
    account_name = account.get('name', '未命名账号')
    card_list_cookie_url = account.get('card_list_cookie_url')

    if not card_list_cookie_url:
        logger.error(f"{account_name}: 未配置 card_list_cookie_url")
        return

    logger.info(f"开始处理账号: {account_name}")
    
    headers = {
        'Host': 'api.weibo.cn',
        'Accept': '*/*',
        'X-Sessionid': '6D340DD7-0F9C-4F09-9DCA-D0E36ABE5CCA',
        'User-Agent': 'WeiboOverseas/6.7.1 (com.weibo.international; build:6.7.1.1; iOS 18.3.0) Alamofire/5.10.2',
        'Accept-Language': 'zh-Hans-US;q=1.0, en-US;q=0.9, zh-Hant-US;q=0.8, fr-US;q=0.7, nl-US;q=0.6',
        'Accept-Encoding': 'json',
        'Connection': 'keep-alive'
    }

    since_id = 1
    params = extract_params(card_list_cookie_url)
    params['card_list_cookie_url'] = card_list_cookie_url
    card_type_11_info = get_card_type_11(params, headers, since_id)

    if not card_type_11_info:
        logger.warning(f"{account_name}: 没有获取到数据")
        return

    super_topic_list = "\n".join([f"    {info['title_sub']}" for info in card_type_11_info])
    logger.info(f"{account_name} 超话列表：")
    logger.info("\n"+super_topic_list)

    logger.info(f"{account_name} 签到结果：")
    result_message = "\n"
    for info in card_type_11_info:
        if info['signin_status']:
            result_message += f"    {info['title_sub']}：✅ 已签到\n"
        else:
            result = sign_in(headers, params, info['scheme'], since_id)
            if result and result.get('msg') == '已签到':
                state = '✅ 成功'
            else:
                state = '❌ 失败'
            result_message += f"    {info['title_sub']}超话：{state}\n"
            time.sleep(random.randint(5, 10))
    
    logger.info(result_message)
    send_bark(f"{account_name}微博超话签到", result_message)
    return result_message

if __name__ == "__main__":
    logger.info("开始执行微博超话签到任务")
    logger.info(f"共有 {len(WEIBO_ACCOUNTS)} 个账号需要处理")
    
    all_results = []
    for account in WEIBO_ACCOUNTS:
        try:
            result = process_account(account)
            if result:
                all_results.append(result)
            time.sleep(random.randint(10, 20))  # 账号之间添加随机延迟
        except Exception as e:
            logger.error(f"处理账号 {account.get('name', '未命名账号')} 时发生错误: {str(e)}")
            continue
    
    # 发送总结通知
    if all_results:
        summary = "\n=================\n".join(all_results)
        send_bark("微博超话签到汇总", summary)
    
    logger.info("所有账号处理完成")