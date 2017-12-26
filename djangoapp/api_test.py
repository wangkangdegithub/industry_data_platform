class Mingrenmingyan:
    """
    处理IP定位 接口返回的数据
    """
    def __init__(self):
        """
        初始化相关数据,包括接口的url,headers和parm
        :return: None
        """
        self.url = 'http://restapi.amap.com/v3/ip?key=b55e49c33bd3a93081481980973aefab&'

    def get_mrmy(self):
        """
        从接口获取定位数据,,返回json数据.
        :return:json, ip定位数据
        """
        wb_data = requests.get(self.url, headers=self.headers, params=self.parm)
        data = wb_data.json()
        if data['error_code'] == 0:
            result = data['result']
            random_num = random.randint(0, 19)
            return json.dumps(result[random_num])
        else:
            return json.dumps(data)

