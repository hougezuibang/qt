import webbrowser

# 指定 HTML 文件的路径
file_path = '1.html'

try:
    # 指定浏览器
    browser = webbrowser.get('microsoft-edge')  # 或者 'firefox', 'ie', 等
    
    # 打开 HTML 文件
    browser.open(file_path)
except webbrowser.Error as e:
    print(f"无法打开浏览器: {e}")
except Exception as e:
    print(f"发生未知错误: {e}")
