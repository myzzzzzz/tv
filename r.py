# 导入测试所需的模块和函数
from ts import get_epgs_rthkradio, get_channels_rthkradio

# 编写测试函数
def test_get_channels_rthkradio():
    # 执行 get_channels_rthkradio 函数
    channels = get_channels_rthkradio()
    
    # 编写断言来验证结果
    assert len(channels) > 0  # 频道列表不为空

def test_get_epgs_rthkradio():
    # 准备测试参数
    channel_id = 1  # 替换为你要测试的频道ID
    date = datetime.datetime(2023, 10, 31)  # 替换为你要测试的日期
    func_arg = None  # 替换为其他参数

    # 执行 get_epgs_rthkradio 函数
    result = get_epgs_rthkradio(channel_id, date, func_arg)
    
    # 编写断言来验证结果
    assert result['success'] == 1  # 确保成功标志为1
    assert len(result['epgs']) > 0  # 确保节目单信息不为空

# 运行测试函数
if __name__ == "__main__":
    test_get_channels_rthkradio()
    test_get_epgs_rthkradio()