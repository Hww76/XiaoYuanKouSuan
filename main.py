from mitmproxy import http
import json
from mitmproxy.tools.main import mitmdump
import sys
import threading
import os
import subprocess
import number_command
import time
import tkinter as tk
from tkinter import messagebox
import argparse
import getExerciseJs
# CONFIG #
tick_time = 0.3    # 每题间隔时间
start_time = 12.5    # 开始做题前摇时间


def request(flow: http.HTTPFlow) -> None:
    # 处理请求
    # print(f"Request: {flow.request.method} {flow.request.url}")
    pass

def response(flow: http.HTTPFlow) -> None:
    # 处理响应

    print(f"Response: {flow.response.status_code} {flow.request.url}")

    ''' 原方案
    # 如果url中包含指定的关键字，则打印响应信息
    if "https://xyks.yuanfudao.com/leo-math/android/exams?" in flow.request.url:
        # 将响应信息转换为json格式
        answer = json.loads(flow.response.text)
        # 格式化输出
        print(json.dumps(answer, indent=4))
        # 保存到文件
        # with open("answer.json", "w") as f:
        #     f.write(json.dumps(answer, indent=4))
        select_answer(answer,"练习")
    elif "https://xyks.yuanfudao.com/leo-game-pk/android/math/pk/match?" in flow.request.url:
        # 将响应信息转换为json格式
        answer = json.loads(flow.response.text)
        # 格式化输出
        print(json.dumps(answer, indent=4))
        # 保存到文件
        # with open("answer.json", "w") as f:
        #     f.write(json.dumps(answer, indent=4))
        select_answer(answer,"pk")
    
    '''

    if "https://leo.fbcontent.cn/bh5/leo-web-oral-pk/exercise_" in flow.request.url:
        # 初始化 text 变量
        text = None
    
    # 查询本地是否有 exercise.js
        try:
            with open("exercise.js", "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            # 如果没有则下载
            print("未找到 exercise.js，正在下载")
            with open("original.js", "w", encoding="utf-8") as f:
                f.write(flow.response.text)
            getExerciseJs.replace_and_change_js("original.js", "exercise.js")
        
            # 重新读取生成的 exercise.js
            with open("exercise.js", "r", encoding="utf-8") as f:
                text = f.read()
    
        # 确保 text 变量有值
        if text is not None:
            flow.response.text = text
            print("修改成功")
        else:
            print("未能修改响应文本")

    

def answer_write(answer):
    
    for i in range(len(answer)):
        number_command.swipe_screen(answer[i])
        # time.sleep(0.16)
        time.sleep(0.3)

def select_answer(answer, type):
    # 关闭notepad
    # os.system("taskkill /f /im notepad.exe")

    # 并保存到txt文件
    f = open("answer.txt", "w")

    select_answer = []

    if type == "练习":
        for question in answer["questions"]:
            answers=question["answers"]
            for i in range(len(answers)):
                if "." in answers[i]:
                    correct_answer = answers[i]
                    break
                if i == len(answers)-1:
                    correct_answer = answers[0]
                
            select_answer.append(correct_answer)
            print(correct_answer, end="  ")
            f.write(str(correct_answer) + "  ")
    elif type == "pk":
        for question in answer["examVO"]["questions"]:
            answers=question["answers"]
            for i in range(len(answers)):
                if "." in answers[i]:
                    correct_answer = answers[i]
                    break
                if i == len(answers)-1:
                    correct_answer = answers[0]
                
            select_answer.append(correct_answer)
            print(correct_answer, end="  ")
            f.write(str(correct_answer) + "  ")
    
    # 关闭文件
    f.close()

    q_num = len(select_answer)
    threading.Thread(target=gui_answer, args=(select_answer,q_num,)).start()

    # 用记事本打开文件
    # os.system("notepad answer.txt")
    # threading.Thread(target=os.system, args=("notepad answer.txt",)).start()
    
def gui_answer(answer,q_num):
    # 创建一个GUI
    root = tk.Tk()
    root.title("继续执行")
    
    def on_button_click():
        answer_write(answer)  # 继续执行代码

    def on_button2_click():
        number_command.next_round()  # 继续执行代码
        root.destroy()
    
    # 创建一个按钮
    button = tk.Button(root, text="点击继续", command=on_button_click)
    button2 = tk.Button(root, text="下一把", command=on_button2_click)
    button.pack(pady=20)
    button2.pack(pady=20)
    
    # 设置定时器，若干秒后自动点击按钮
    time = int(start_time * 1000)
    root.after(time, on_button_click)
    time2 = int((start_time + tick_time * 1.15 * q_num + 5) * 1000)
    root.after(time2, on_button2_click)
    # 运行 GUI 界面
    root.mainloop()

    # time.sleep(4)
    # answer_write(answer)
    # time.sleep(7)
    # command = "input tap 1445 1272"
    # number_command.run_adb_command(command)
    # time.sleep(0.1)
    # command = "input tap 2144 1694"
    # number_command.run_adb_command(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mitmproxy script")
    parser.add_argument("-P", "--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("-H", "--host", type=str, default="0.0.0.0", help="Host to listen on")
    args = parser.parse_args()

    sys.argv = ["mitmdump", "-s", __file__, "--listen-host", args.host, "--listen-port", str(args.port)]

    mitmdump()

# 这段代码主要是通过`mitmproxy`工具进行网络代理，拦截特定的网络请求并对响应进行处理，同时结合图形用户界面（GUI）实现一些特定的功能，其主要用途包括以下几个方面：

# **一、网络请求拦截与响应处理**

# 1. **拦截特定 URL 的响应**：
#    - 代码会监听网络请求，当请求的 URL 中包含`https://leo.fbcontent.cn/bh5/leo-web-oral-pk/exercise_`时，会进行特殊处理。
#    - 首先尝试从本地读取`exercise.js`文件，如果文件不存在，则将该请求的响应内容写入`original.js`文件，然后通过调用`getExerciseJs.replace_and_change_js`函数对`original.js`进行处理并生成`exercise.js`文件。
#    - 最后，如果成功读取到`exercise.js`文件的内容，则将拦截到的请求的响应内容替换为`exercise.js`的内容，实现对特定请求的响应修改。

# **二、答案提取与保存**

# 1. **从响应中提取答案**：
#    - 对于不同类型的请求（目前区分了“练习”和“pk”两种类型），如果请求的 URL 中包含特定关键字，代码会将响应转换为 JSON 格式，并从 JSON 数据中提取答案。
#    - 在“练习”类型中，遍历响应中的`questions`列表，对于每个问题，从`answers`列表中查找包含点号的答案作为正确答案，如果没有找到则取第一个答案。
#    - 在“pk”类型中，类似地遍历`examVO["questions"]`列表提取答案。

# 2. **保存答案并提供可视化操作**：
#    - 将提取到的答案保存到`answer.txt`文件中，并在控制台打印答案。
#    - 启动一个图形用户界面（GUI）窗口，窗口中有“点击继续”和“下一把”两个按钮。
#    - “点击继续”按钮触发时，会调用`answer_write`函数，根据提取的答案执行一些操作（可能与答题相关，具体取决于`number_command.swipe_screen`函数的功能）。
#    - “下一把”按钮触发时，会调用`number_command.next_round`函数，可能是进行下一轮操作，然后关闭 GUI 窗口。

# **三、自动化操作与定时功能**

# 1. **自动化答题流程**：
#    - 通过设置定时器，在程序启动一段时间后（由`start_time`变量控制）自动触发“点击继续”按钮的操作，模拟用户点击，执行答题相关的代码。
#    - 根据答案数量和每题间隔时间（`tick_time`变量）计算时间，在一定时间后自动触发“下一把”按钮的操作，进行下一轮操作或关闭当前流程。

# 综上所述，这段代码的主要用途是拦截特定网络请求、提取答案、保存答案并提供可视化操作界面，同时通过自动化和定时功能实现一定程度的答题自动化流程。


# 以下是对这段代码执行流程的详细分析：

# **一、模块导入**
# 1. 首先导入了多个模块，包括：
#    - `mitmproxy`的`http`模块，用于处理 HTTP 请求和响应。
#    - `json`模块，用于处理 JSON 数据格式。
#    - `mitmproxy.tools.main`中的`mitmdump`，可能用于启动代理服务。
#    - `sys`模块，用于与 Python 解释器进行交互。
#    - `threading`模块，用于实现多线程编程。
#    - `os`模块，用于与操作系统进行交互。
#    - `subprocess`模块，用于创建子进程。
#    - `number_command`模块，推测是自定义模块，用于执行特定的命令。
#    - `time`模块，用于处理时间相关的操作。
#    - `tkinter`模块和其下的`messagebox`，用于创建图形用户界面。
#    - `argparse`模块，用于解析命令行参数。
#    - `getExerciseJs`模块，自定义模块，可能用于处理 JavaScript 文件。

# **二、定义配置变量**
# 1. 定义了两个配置变量：
#    - `tick_time`设置为`0.3`，表示每题的间隔时间。
#    - `start_time`设置为`12.5`，表示开始做题前的等待时间。

# **三、定义函数**
# 1. `request`函数：
#    - 这个函数用于处理 HTTP 请求。目前函数内只是一个占位符，没有具体的实现代码。
#    - 参数`flow`是`http.HTTPFlow`类型，表示一个 HTTP 请求和响应的流。

# 2. `response`函数：
#    - 处理 HTTP 响应。
#    - 首先打印响应的状态码和请求的 URL。
#    - 如果响应的 URL 中包含特定字符串`https://leo.fbcontent.cn/bh5/leo-web-oral-pk/exercise_`：
#      - 初始化变量`text`为`None`。
#      - 尝试读取本地文件`exercise.js`，如果文件不存在，则将响应内容写入`original.js`文件，然后调用`getExerciseJs.replace_and_change_js`函数处理`original.js`并生成`exercise.js`，最后重新读取`exercise.js`。
#      - 如果`text`不为`None`，则将响应内容替换为`text`，并打印“修改成功”，否则打印“未能修改响应文本”。

# 3. `answer_write`函数：
#    - 接受一个答案列表作为参数。
#    - 遍历答案列表，对于每个答案调用`number_command.swipe_screen`函数，可能是执行某种与答案相关的操作，并在每次循环中暂停`0.3`秒。

# 4. `select_answer`函数：
#    - 接受一个答案对象和一个类型参数。
#    - 关闭记事本程序（如果正在运行）。
#    - 打开`answer.txt`文件用于写入。
#    - 根据传入的类型参数，遍历答案对象中的问题和答案列表，找到包含点号的答案作为正确答案，如果没有找到则取第一个答案，并将正确答案添加到`select_answer`列表中，同时打印并写入到文件中。
#    - 关闭文件。
#    - 计算答案数量`q_num`。
#    - 启动一个新线程，调用`gui_answer`函数并传入答案列表和答案数量。

# 5. `gui_answer`函数：
#    - 创建一个图形用户界面（GUI）窗口。
#    - 定义两个按钮的点击事件函数：
#      - `on_button_click`函数调用`answer_write`函数继续执行代码。
#      - `on_button2_click`函数调用`number_command.next_round`函数并销毁窗口。
#    - 创建两个按钮并设置布局。
#    - 设置定时器，在一定时间后自动点击按钮。第一个定时器在`start_time`毫秒后触发`on_button_click`，第二个定时器在`start_time + tick_time * 1.15 * q_num + 5`毫秒后触发`on_button2_click`。
#    - 运行 GUI 界面，进入主循环等待用户交互。

# **四、主程序部分**
# 1. 在`if __name__ == "__main__":`条件下执行以下代码：
#    - 创建一个`argparse.ArgumentParser`对象，用于解析命令行参数。定义了`-P`/`--port`参数表示监听的端口号，默认值为`8080`；定义了`-H`/`--host`参数表示监听的主机地址，默认值为`0.0.0.0`。
#    - 解析命令行参数并存储在`args`变量中。
#    - 修改`sys.argv`，设置为启动`mitmdump`的命令行参数，包括指定脚本文件、监听主机地址和端口号。
#    - 调用`mitmdump`函数，启动代理服务，开始监听指定的主机和端口，当有 HTTP 请求和响应时，会调用前面定义的`request`和`response`函数进行处理。