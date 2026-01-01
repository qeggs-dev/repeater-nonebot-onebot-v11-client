# @复读机Repeater
**- Only Chat, Focus Chat. -**

*注：本仓库仅为客户端实现，需要配合[后端项目](#相关仓库)使用*

一个基于[`NoneBot`](https://nonebot.dev/)和[`Repeater Backend`](https://github.com/qeggs-dev/repeater-ai-chatbot-backend)开发的 AI QQ Bot
**此仓库仅为 Repeater 的 NoneBot OneBot v11 适配客户端**

---

## Length Score
长度评分系统，用于判断回复是否过长，过长则自动发送图片
长度评分的参数由`main_api.json/text_length_score_config`定义，其包含以下参数：
 - `max_lines`：回复的最大行数
 - `single_line_max`：单行的最大长度
 - `mean_line_max`：平均行的最大长度
 - `total_length`：总长度
 - `threshold`：长度评分阈值，包含`group`和`private`两个参数，分别表示群聊和私聊的阈值

长度评分系统通过以下公式计算：
```python
def length_score(text: str) -> float:
    if len(text) == 0:
        length_score = 0
    else:
        lines = text.splitlines()
        length_score = (
            len(lines) / max_lines +
            (
                max(len(line) for line in lines) / single_line_max +
                sum(len(line) for line in lines) / len(lines) / mean_line_max
            ) / 2 +
            len(text) / total_length
        ) / 3
    return length_score
```
PS: 此处的长度评分函数并非实际算法，仅为演示使用
如果长度评分超过阈值，则会向后端请求将文本渲染为图片，以保证不会影响其他用户正常聊天。

---

## ENV配置

| Name                         | Default                                                                    | Description |
|------------------------------|----------------------------------------------------------------------------|-------------|
| REPEATER_LOGGER_LEVEL        | "INFO"                                                                     | 日志等级，可选值：`TRACE`, `DEBUG`、`INFO`、`WARNING`、`ERROR`、`CRITICAL` |
| REPEATER_LOGGER_FORMAT       | "{time:YYYY-MM-DD HH:mm:ss.SSS} \| {level} \| {extra[module]} - {message}" | 到文件的日志格式，与控制台无关 |
| REPEATER_LOGGER_PATH         | "logs/repeater-log-{time:YYYY-MM-DD-HH-mm-ss}.log"                         | 日志文件的路径 |
| REPEATER_LOGGER_ENABLE_QUEUE | true                                                                       | 是否启用队列模式 |
| REPEATER_LOGGER_DELAY        | true                                                                       | 是否在第一条日志输出时才创建日志文件 |
| REPEATER_LOGGER_ROTATION     | "100 MB"                                                                   | 日志文件的轮换条件，可填时长、大小等数据 |
| REPEATER_LOGGER_RETENTION    | "1 month"                                                                  | 日志文件的保留条件，可填时长、大小等数据 |
| REPEATER_LOGGER_COMPRESSION  | "zip"                                                                      | 日志文件的处理方式 |
| STORAGE_BASE_PATH            | "./storage"                                                                | 存储文件的基础路径 |
| ENVIRONMENT                  | "dev"                                                                      | 该值的内容将决定了程序会进一步读取哪个环境变量文件，如`prod`就是读取`.env.prod`，`dev`就是读取`.env.dev` |
| HOST                         | "0.0.0.0"                                                                  | 主机地址 |
| PORT                         | 8080                                                                       | 端口号 |
| COMMAND_START                | ["/"]                                                                      | 用于触发命令的开始字符 |
| COMMAND_SEP                  | ["."]                                                                      | 用于触发命令的分隔符 |
| ONEBOT_ACCESS_TOKEN          | ""                                                                         | OneBot的访问令牌 |
| SUPERUSERS                   | [""]                                                                       | 超级用户列表 |

---

## License
这个项目基于[MIT License](LICENSE)发布。

---

## 依赖
| Name       | Version | License      | License Text Link                                                      | Where it is used              |
|------------|---------|--------------|------------------------------------------------------------------------|-------------------------------|
| httpx      | 0.28.1  | BSD License  | [BSD-3-Clause](https://github.com/encode/httpx/blob/master/LICENSE.md) | *Entire Project*              |
| nonebot    | 2.4.3   | MIT License  | [MIT](https://github.com/nonebot/nonebot2/blob/master/LICENSE)         | *Entire Project*              |
| pydantic   | 2.12.0  | MIT License  | [MIT](https://github.com/pydantic/pydantic/blob/main/LICENSE)          | *Entire Project*              |
| aiofiles   | 25.1.0  | MIT License  | [Apache-2.0](https://github.com/Tinche/aiofiles/blob/main/LICENSE)     | `storage`                     |
| pyyaml     | 6.0.3   | MIT License  | [MIT](https://github.com/yaml/pyyaml/blob/main/LICENSE)                | `storage`                     |
| orjson     | 3.11.3  | Apache Software License; MIT License | [Apache-2.0](https://github.com/ijl/orjson/blob/master/LICENSE-APACHE) / [MIT](https://github.com/ijl/orjson/blob/master/LICENSE-MIT) | `storage` |
| loguru     | 0.7.3   | MIT License  | [MIT](https://github.com/Delgan/loguru/blob/master/LICENSE)            | *Entire Project*              |

具体依赖的License请查看[LICENSES.md](LICENSES.md)

---

## 配置部署
**推荐Python3.11以上版本安装**
> PS: 复读机可能会兼容Python3.11以前的版本
> 但我们并未对其进行过测试
> 此处3.11为开发环境版本

在目录下执行 `setup.bat` 或 `bash setup.sh`
#### 使用脚手架(nb-cli)创建项目环境
1. 选择simple模板
2. 给项目起个名字（比如`Repeater`）
3. 建议使用FastAPI驱动器
4. **至少必须选择OneBot V11适配器**
5. 输入Yes安装默认依赖
6. 输入Yes安装虚拟环境
7. 如果需要，可以选择内置插件，如echo，*但如果没记错的话我们好像有一个echo了*
8. 在项目目录下，找到`.env`文件
9. 填写 `PORT`(数字), `ONEBOT_ACCESS_TOKEN`(字符串) 等字段配置项
10. 将复读机的NoneBot插件放入项目目录下（通常是`plugins`文件夹下）

执行`{项目名称}/.venv/pip install httpx`安装唯一依赖（此处这个大括号要去掉）
运行`run.py`启动程序

---

## 连接

### 连接OneBot
1. 找到项目目录下的`.env`文件
2. 填写PORT(数字), ONEBOT_ACCESS_TOKEN(字符串) 等字段配置项
3. 执行`run.bat`或`bash run.sh`启动程序
4. 打开OneBot客户端，选择反向WebSocket(部分客户端上称为`WebSocket 客户端`)
5. 填写 `ws_url`(字符串，通常是`ws://127.0.0.1:PORT`，其中`PORT`是你在`.env`文件中填写的端口号)，`token`(字符串，需要与上面的`ONEBOT_ACCESS_TOKEN`一致)
6. 看到NoneBot日志输出中出现`connection open`时, 表示连接成功

### 链接后端
1. 找到项目目录下的`.env`文件
2. 填写`BACKEND_HOST`和`BACKEND_PORT`字段配置项 (其中HOST是后端服务主机的IP地址，PORT是后端服务主端口号，需要你和后端配置中编写的一致)
3. 执行`run.bat`或`bash run.sh`启动程序

PS: 由于OneBot客户端通常为入站服务，所以默认情况下所有服务都不需要配置公网IP访问
但你需要保证后端可以连接到你设定的API端口，OneBot客户端可以连接到指定社交平台的服务器

---

## Markdown图片渲染样式

| 风格 | 译名 |
| --- | :---: |
| **`light`** | 亮色 |
| `dark` | 暗色 |
| `red` | 红色 |
| `pink` | 粉色 |
| `blue` | 蓝色 |
| `green` | 绿色 |
| `purple` | 紫色 |
| `yellow` | 黄色 |
| `orange` | 橙色 |
| `dark-red` | 暗红色 |
| `dark-pink` | 暗粉色 |
| `dark-blue` | 暗蓝色 |
| `dark-green` | 暗绿色 |
| `dark-purple` | 暗紫色 |
| `dark-yellow` | 暗黄色 |
| `dark-orange` | 暗橙色 |
| `legacy` | 旧版亮色 |
| `legacy-dark` | 旧版暗色 |
| `legacy-red` | 旧版红色 |
| `legacy-pink` | 旧版粉色 |
| `legacy-blue` | 旧版蓝色 |
| `legacy-green` | 旧版绿色 |
| `legacy-purple` | 旧版紫色 |
| `legacy-yellow` | 旧版黄色 |
| `legacy-orange` | 旧版橙色 |
| `legacy-dark-red` | 旧版暗红色 |
| `legacy-dark-pink` | 旧版暗粉色 |
| `legacy-dark-blue` | 旧版暗蓝色 |
| `legacy-dark-green` | 旧版暗绿色 |
| `legacy-dark-purple` | 旧版暗紫色 |
| `legacy-dark-yellow` | 旧版暗黄色 |
| `legacy-dark-orange` | 旧版暗橙色 |

PS: `light`为默认风格，无需指定
颜色风格默认在 `./configs/style` 文件夹下

---

## 模板系统

模板系统的部分由后端定义，请参考后端的README。

---

## 配置文件

main_api.json
```json
{
    // Text Length Score 配置
    "text_length_score_config":{
        // 最大长度阈值
        "max_lines": 5,
        // 每行最大字符数
        "single_line_max": 64,
        // 平均行最大字符数
        "mean_line_max": 32,
        // 总字符数
        "total_length": 400,

        // 评分阈值
        "threshold": {
            // 群聊阈值
            "group": 1.0,
            // 私聊阈值
            "private": 2.64
        }
    },
    // 后端推理模型使用的UID
    "reason_model_uid": "reasoner",
    // 在仅@且没有任何文本的情况下
    // 返回的消息内容
    "hello_content": "Repeater is Online!",
    // 是hello_content的变种
    // 这里的Key是星期
    // Value是星期对应的消息内容
    "welcome_messages_by_weekday": {
        "4": "Repeater is Online!\n\n疯狂星期四! ! !\n复读机想要 50,000,000 Token ，求求了（>^< ;)"
    },
    // 是否在群聊中让所有人使用同一个User_ID
    "merge_group_id": false,

    // Repeater API超时时间
    "server_api_timeout": {
        "chat": 600.0,
        "context": 10.0,
        "prompt": 10.0,
        "config": 10.0,
        "variable_expansion": 40.0,
        "render": 600.0
    },

    // 在用户输入图片的时候，是否将其下载为 Base64 以防止链接失效
    "use_base64_visual_input": true
}
```
配置了一些主要的参数，如文本长度评分、推理模型使用的UID、欢迎消息等。

tts.json
```json
{
    // ChatTTS API 地址
    "base_url": "http://127.0.0.1:9966",
    // ChatTTS API 参数
    "api_args": {
        // 模型名称
        "voice": "265.pt",
        // TTS 语速
        "speed": 6,
        // TTS 模型提示词
        "tts_prompt": "[break_6]",
        // TTS 模型温度
        "temperature": 0.2,
        // TTS 模型Top_P
        "top_p": 0.701,
        // TTS 模型Top_K
        "top_k": 20,
        // TTS 模型生成的最大优化Token数
        "refine_max_new_token": 384,
        // TTS 模型生成最大推理Token数
        "infer_max_new_token": 2048,
        // TTS 语速(我不知道为什么会有两个，所以就全都加上了)
        "text_seed": 42,
        // 是否跳过输入优化
        "skip_refine": true,
        // 是否为流式输出
        "is_stream": false,
        // 自定义语音
        "custom_voice": 0
    },
    "timeout": 300.0
}
```
PS：该配置文件是专门用于对接ChatTTS的
如果不需要TTS功能，该部分可以忽略

---

## 命令表

| Command                    | Abridge | Full Name                 | Type        | Joined Version | Description                   | Parameter Description                     | Remarks |
| :---                       | :---    | :---                      | :---:       | :---:          | :---:                         | :---:                                     | :---:   |
| ` `                        | ` `     | ` `                       | `CHAT`      | 4.0 Beta       | 默认命令，自然语言对话          | 自然语言输入                               | 当你@复读机的时候，如果没有命中其他命令就会执行这个，并把所有内容作为输入 |
| `chat`                     | `c`     | `Chat`                    | `CHAT`      | 4.0 Beta       | 与机器人对话                   | 自然语言输入                               | 强制模型用文字输出，绕过Markdown渲染检查 |
| `keepAnswering`            | `ka`    | `KeepAnswering`           | `CHAT`      | 4.0 Beta       | 持续对话(常规)                 | 无                                        | 无须输入，AI再次回复 |
| `keepReasoning`            | `kr`    | `KeepReasoning`           | `CHAT`      | 4.0 Beta       | 持续对话(推理)                 | 无                                        | 无须输入，AI再次使用推理回复 |
| `renderChat`               | `rc`    | `RenderChat`              | `CHAT`      | 4.0 Beta       | 渲染Markdown回复               | 自然语言输入                               | 强制渲染图片输出 |
| `setRenderStyle`           | `srs`   | `SetRenderStyle`          | `CONFIG`    | 4.0 Beta       | 设置渲染样式                   | [渲染样式](#Markdown图片渲染样式)           | 设置Markdown图片渲染样式 |
| `npChat`                   | `np`    | `NoPromptChat`            | `CHAT`      | 4.0 Beta       | 不加载提示词进行对话            | 自然语言输入                               | 使用常规模型 |
| `reason`                   | `r`     | `Reason`                  | `CHAT`      | 4.0 Beta       | 使用Reasoner模型进行推理        | 自然语言输入                               | 调用模型由`reason_model_uid`字段控制，默认`reasoner` |
| `setFrequencyPenalty`      | `sfp`   | `SetFrequencyPenalty`     | `CONFIG`    | 4.0 Beta       | 设置频率惩罚                   | `-2`\~`2`的浮点数<br/>或`-200%`\~`200%`的百分比 | 控制着模型输出重复相同内容的可能性 |
| `setPresencePenalty`       | `spp`   | `SetPresencePenalty`      | `CONFIG`    | 4.0 Beta       | 设置存在惩罚                   | `-2`\~`2`的浮点数<br/>或`-200%`\~`200%`的百分比 | 控制着模型谈论新主题的可能性 |
| `setTemperature`           | `st`    | `SetTemperature`          | `CONFIG`    | 4.0 Beta       | 设置温度                       | `0`\~`2`的浮点数<br/>或`0%`\~`200%`的百分比  | 控制着模型生成内容的不确定性 |
| `setPrompt`                | `sp`    | `SetPrompt`               | `PROMPT`    | 4.0 Beta       | 设置提示词                     | 自然语言输入                               | 设置提示词 |
| `changeDefaultPersonality` | `cdp`   | `ChangeDefaultPersonality`| `CONFIG`    | 4.0 Beta       | 修改默认人格                   | [人格预设](#人格预设)                       | 修改默认人格路由 |
| `deletePrompt`             | `dp`    | `DeletePrompt`            | `PROMPT`    | 4.0 Beta       | 删除提示词                     | 无                                        | 删除提示词 |
| `deleteContext`            | `dc`    | `DeleteContext`           | `CONTEXT`   | 4.0 Beta       | 删除上下文                     | 无                                        | 删除上下文 |
| `varExpand`                | `ve`    | `VarExpand`               | `VAREXPAND` | 4.0 Beta       | 变量展开                       | 文本模板(使用大括号作为[变量](#变量表)标记)  | 变量展开 |
| `setDefaultModel`          | `sdm`   | `SetDefaultModel`         | `CONFIG`    | 4.0 Beta       | 设置默认模型                   | [模型](#模型)                              | 设置默认使用的模型 |
| `setTopP`                  | `stp`   | `SetTopP`                 | `CONFIG`    | 4.0.1 Beta     | 设置Top_P参数                  | 0\~1的浮点数<br/>或`0%`\~`100%`的百分比    | 设置Top_P参数 |
| `setMaxTokens`             | `stm`   | `SetMaxTokens`            | `CONFIG`    | 4.0.1 Beta     | 设置最大生成tokens数           | 0\~4096的整数                              | 设置最大生成tokens数 |
| `getContextTotalLength`    | `gctl`  | `GetContextTotalLength`   | `CONTEXT`   | 4.0.1 Beta     | 获取上下文总长度               | 无                                         | 获取上下文总长度 |
| `publicSpaceChat`          | `psc`   | `PublicSpaceChat`         | `CHAT`      | 4.0.2.1 Beta   | 公共空间聊天                   | 自然语言输入                                | 公共空间聊天 |
| `deletePublicSpaceContext` | `dpsc`  | `DeletePublicSpaceContext`| `CONTEXT`   | 4.0.2.1 Beta   | 删除公共空间上下文             | 无                                         | 删除公共空间上下文 | 
| `sendUserDataFile`         | `sudf`  | `SendUserDataFile`        | `USERFILE`  | 4.0.2.1 Beta   | 发送用户数据文件               | 无                                         | 发送用户数据文件 |
| `changeContextBranch`      | `ccb`   | `ChangeContextBranch`     | `CONTEXT`   | 4.1.2.0        | 切换上下文分支                 | 分支名称                                   | 切换上下文分支 |
| `changePromptBranch`       | `cppb`  | `ChangePromptBranch`      | `PROMPT`    | 4.1.2.0        | 切换提示词分支                 | 分支名称                                   | 切换提示词分支 |
| `changeConfigBranch`       | `ccfgb` | `ChangeConfigBranch`      | `CONFIG`    | 4.1.2.0        | 切换配置分支                   | 分支名称                                   | 切换配置分支 |
| `reference`                | `ref`   | `Reference`               | `CHAT`      | 4.1.2.0        | 引用上下文                     | @群成员并输入自然语言                       | 引用其他用户的上下文进行生成，并将结果保存到自己的聊天记录中 |
| `chooseGroupMember`        | `cgm`   | `ChooseGroupMember`       | `OTHER`     | 4.1.2.0        | 抽取群组成员                   | 抽取数量                                   | 抽取群组成员 |
| `withdraw`                 | `w`     | `Withdraw`                | `CONTEXT`   | 4.2.3.0        | 撤回消息                       | 无                                        | 删除复读机上下文中保存的最新一回合对话 |
| `recentSpeakingRanking`    | `rsr`   | `RecentSpeakingRanking`   | `OTHER`     | 4.2.3.0        | 最近发言排行                   | 无                                        | 获取群组内最近发言的成员列表 |
| `setAutoShrinkLength`      | `sasl`  | `SetAutoShrinkLength`     | `CONFIG`    | 4.2.4.0        | 设置自动缩减长度上限            | 整数                                      | 如果你的聊天条数超过该值，系统会尝试自动删除最旧的部分 |
| `deleteSession`            | `ds`    | `DeleteSession`           | `MIXED`     | 4.2.5.0        | 删除所有用户数据               | 无                                        | 删除所有用户数据 |
| `raw`                      | `raw`   | `Raw`                     | `CHAT`      | 4.2.5.1        | 发送消息且不包含任何元数据      | 自然语言输入                               | 发送消息且不包含任何元数据 |
| `changeSession`            | `cs`    | `ChangeSession`           | `MIXED`     | 4.2.5.1        | 让所有的数据同时切换到一个分支   | 分支名称                                  | 让`Context`、`Prompt`、`Config`同时切换到一个分支 |
| `noSaveChat`               | `nsc`   | `NoSaveChat`              | `CHAT`      | 4.2.6.6        | 不保存的聊天对话                | 无                                        | 聊天后不保存最新聊天记录 |
| `summaryChatRecord`        | `scr`   | `SummaryChatRecord`       | `OTHER`     | 4.2.6.6        | 聊天记录总结                    | 整数，传入的消息数量                       | 获取当前群聊内指定数量的聊天记录摘要 |
| `varExpandText`            | `vet`   | `Var_Expand_Text`         | `VAREXPAND` | 4.2.7.0        | 变量展开                       | 文本模板(使用大括号作为[变量](#变量表)标记)  | 强制使用文本输出 |
| `varExpandImage`           | `vei`   | `Var_Expand_Image`        | `VAREXPAND` | 4.2.7.0        | 变量展开                       | 渲染模板(使用花括号作为[变量](#变量表)标记)  | 强制使用图片输出 |
| `setAutoLoadPrompt`        | `salp`  | `SetAutoLoadPrompt`       | `CONFIG`    | 4.3.1.0        | 设置自动加载提示词              | `true`或`false`                           | 设置请求时是否自动加载Prompt |
| `setAutoSaveContext`       | `sasc`  | `SetAutoSaveContext`      | `CONFIG`    | 4.3.1.0        | 设置自动保存上下文              | `true`或`false`                           | 设置生成完毕后是否自动保存Context |
| `setRenderTitle`           | `srt`   | `SetRenderTitle`          | `CONFIG`    | 4.3.2.1        | 设置渲染标题                    | 任意文本                                   | 渲染时显示的标题内容 |
| `setTimezone`              | `stz`   | `SetTimezone`             | `CONFIG`    | 4.3.3.3        | 设置时区                        | 时区名称(如`Asia/Shanghai`)                | 请使用确定的时区名称 |
| `writeUserProfile`         | `wup`   | `WriteUserProfile`        | `CONFIG`    | 4.3.3.6        | 写入用户人设数据                 | 任意文本                                   | 该部分会被嵌入到用户提示词中，告诉AI用户的基础设定 |
| `setHtmlTemplate`          | `sht`   | `SetHtmlTemplate`         | `CONFIG`    | 4.3.3.6        | 设置HTML模板                    | 预设模板名称                               | 可以用于切换Markdown渲染时使用的HTML模板 |
| `setSaveTextOnly`          | `ssto`  | `SetSaveTextOnly`         | `CONFIG`    | 4.3.6.0        | 是否在保存时丢弃除了文本以外的内容 | `true`或`false`                           | 设为`true`可以更快速的完成保存与读取，但模型将无法再获取之前的附加数据 |
| `textRender`               | `tr`    | `TextRender`              | `Render`    | 4.3.7.0        | Markdown 文本渲染                | Markdown 文本                             | 将 Markdown 文本渲染为图片 |
| `getModelList`             | `gml`   | `GetModelList`            | `MODEL`     | 4.3.7.4        | 获取模型列表                     | 模型类型(目前只有`chat`)                   | 获取模型列表 |
| `generatePrompt`           | `gp`    | `GeneratePrompt`          | `MODEL`     | 4.3.7.5        | 生成提示词                       | 角色描述                                  | 生成提示词，并自动保存到用户提示词数据中 |
| `summarizeAndContract`     | `sac`   | `SummarizeAndContract`    | `CHAT`      | 4.3.7.6        | 摘要并压缩                       | 自定义提示词，可以为空                      | 摘要并压缩对话，并自动删除多余的历史记录 |

PS：`CHAT`类型命令几乎全员支持视觉输入
由于需要保存上下文，复读机默认会将其下载为Base64编码
你可以在配置文件中关闭该选项，这会让复读机直接使用QQ传递的临时URL
适合不保存图片的情况

`MIXED`类型命令同时映射了
Context、Prompt、Config
三种数据类型的API
使用这些命令的时候
后端会同时收到三个API的请求

## 相关仓库
- [Repeater Backend](https://github.com/qeggs-dev/repeater-ai-chatbot)