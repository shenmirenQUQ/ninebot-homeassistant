# Ninebot Home Assistant Custom Integration

这是一个基于旧版九号账号密码链路的 Home Assistant 自定义集成。

## 当前能力

- 在 HA 配置流里直接填写九号账号密码
- 首次配置时自动拉取车辆列表
- 支持选择一台车辆接入
- 提供以下实体：
  - 电量
  - 预计续航
  - 位置
  - 充电状态
  - 开机状态
  - GSM
  - SN

## 安装

把整个 `custom_components/ninebot` 目录复制到 Home Assistant 的 `config/custom_components/` 下。

## 使用

1. 重启 Home Assistant
2. 进入 **设置 → 设备与服务 → 添加集成**
3. 搜索 `Ninebot`
4. 输入账号、密码和语言
5. 如果账号下有多台车，选择要接入的车辆

## 注意

- 当前使用的是已验证可用的旧接口链路：账号密码登录 → access_token → 设备列表 → 设备详情。
- 后续如果九号关闭这条旧链路，需要再迁移到新的 Device Service Key 方案。
