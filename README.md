# Ninebot Home Assistant Integration

九号电动车 / 电摩 Home Assistant 自定义集成，支持在 Home Assistant 中直接使用**账号密码登录**并拉取车辆数据。

> 当前版本基于已验证可用的旧版账号密码链路：账号密码登录 → access_token → 设备列表 → 设备详情。

## 功能

- 在 HA 配置流中直接填写九号账号密码
- 首次配置时自动拉取车辆列表
- 多车时支持选择其中一台接入
- 提供以下实体：
  - 电量
  - 预计续航
  - 位置
  - 充电中
  - 已开机
  - GSM 信号
  - GSM 更新时间
  - 剩余充电时间
  - PWR 状态
  - SN
  - 车辆编号

## 安装

将仓库中的 `custom_components/ninebot` 目录复制到 Home Assistant 配置目录下：

```text
/config/custom_components/ninebot
```

然后重启 Home Assistant。

## 使用

1. 打开 **设置 → 设备与服务**
2. 点击 **添加集成**
3. 搜索 `Ninebot`
4. 输入九号账号、密码和语言
5. 如账号下有多台车，选择要接入的车辆

## 已知限制

- 当前位置接口返回的是文本地址 `locationDesc`，**没有直接返回经纬度**。
- 因此目前提供的是位置文本实体，还不是标准地图定位 `device_tracker`。
- 如果后续发现可用的经纬度接口，可以继续补定位设备支持。

## 目录结构

```text
custom_components/ninebot/
```

## 免责声明

本项目为非官方社区集成，仅供学习研究与个人使用。接口行为可能随九号服务端调整而变化。

## License

MIT
