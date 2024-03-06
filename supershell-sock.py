import os
import platform
import subprocess
import pexpect

def run_auto(host, user, port, r_id, command):
    # 格式化SSH命令
    ssh_command = f"ssh -J {user}@{host}:{port} {r_id} -t '{command}'"
    
    # 运行SSH命令
    child = pexpect.spawn(ssh_command, timeout=60000)

    while True:
        try:
            # 预期SSH首次连接时的指纹认证提示
            i = child.expect(['Are you sure you want to continue connecting (yes/no/[fingerprint])?', pexpect.EOF, pexpect.TIMEOUT])
    
            # 如果出现了指纹认证提示，发送"yes"
            if i == 0:
                child.sendline('yes')
            elif i == 1:
                # SSH命令执行完成
                break
            elif i == 2:
                # SSH命令超时或遇到未预期的错误
                print("SSH command timed out or there was an unexpected error.")
                break
        except pexpect.EOF:
            break
        except pexpect.TIMEOUT:
            print("Timeout occurred.")
            break

    # 获取执行结果
    output = child.before.decode()
    
    # 关闭child进程
    child.close()
    
    # 打印SSH命令的结果
    print(output)
    
    # 返回执行结果，以便进行后续处理
    return output


def save_private_key(rsa_key):
    # 确定操作系统
    os_type = platform.system()
    
    # 设置默认的私钥路径
    if os_type == "Linux" or os_type == "Darwin":
        key_path = os.path.join(os.path.expanduser("~"), ".ssh", "id_rsa")
    elif os_type == "Windows":
        key_path = os.path.join(os.environ["USERPROFILE"], ".ssh", "id_rsa")
    else:
        raise Exception("Unsupported OS")
    
    # 确保.ssh目录存在
    os.makedirs(os.path.dirname(key_path), exist_ok=True)
    
    # 保存私钥
    with open(key_path, "w") as key_file:
        key_file.write(rsa_key)
    
    # 更改私钥文件的权限为600，仅限Linux/MacOS
    if os_type != "Windows":
        os.chmod(key_path, 0o600)
    
    print("Private key saved successfully.")

def execute_ssh_command(command, host, user,port=""):
    # 假设私钥已经位于默认位置，因此不需要显式指定.
    ssh_command =""
    if port:
        ssh_command = f"ssh -p {port} {user}@{host} {command}"
    else:
        ssh_command = f"ssh {user}@{host} {command}"
    
    # 执行SSH命令
    result = subprocess.run(ssh_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if result.stderr:
        print("Error executing SSH command:", result.stderr)
        return ""
    
    return result.stdout


def process_data(data):
    res_id = []
    lines = data.strip().split("\n")
    for line in lines:
        items = line.strip().split()
        if items:
            res_id.append(items[0])
    return res_id


def main():
    rsa_key = r'''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAlocDEVsA37DHol1Pyj2c+R7yv88eHwK6ytJ3ygHMecakDhvy
f8kXPe1sjuaFeQE3xmIVdtkUcDVTOC5cIUxOdZMwnWe0kqLaapJCnv4Sv8O28ZE0
r5H1FxLYbU9qN9RV7wPaBM1qhVJIiQzcNPNVmFmVSlZ7EDXoPOTEbgvWSp8p6FSN
dP+mQ1ikbkHuONi3pQnqYHhiHR3HOiaH9zFea+xpdfpCPEUgvnmzYxIEuRge4+RH
TGkNYiMG5BBesSPZEhwZLA+kVA67m+AEA41vm6NCr4XPrLY6TYOP5Q4DxW60VnLp
Re/g+B/SyYRvgZtzMt36ewCv/Ga0wF5FTubAyQIDAQABAoIBADZNOkQWijgn87yU
4OXaWDhee7/KHdmeCHiGeIQ9JeCAUkpstox2pJXIgrMCYgAG+nHsjEW1hfP8qKrJ
vp6cgmlT0ePWt4N2kEiFvtbQXT8kgWifs1vq0XmjaMP2NCEzzlRNFWdKGzVBO72F
ECNh7Ozq1Dpe/EIa0E63UE1Ko+GC/7pU+hFshum8m4/w3h/9a12uaQLQJm5zNOX2
0TF4cqbSaonZ4lzLBKg6nOrkuut/bkF1/znwEh3v8swfPLEgUscfA5KgGnqr50eB
F2fbUn3m253QN/VafFs8NUwg5MQrd+p7vUMmD3b3uVKMD55qtSFc/6OacGY7y3ae
cowXuwkCgYEAzWFxIVMxVTo4cOcO6ZbNgLp5iI74PrrKSczLFqTB1cLG57a4CnS0
pgTse7gxUB7KLeQ+CmaqhxMoNkOkn4N8Pxmp+pxWih2U4aTw5XANSM5B4rJ/O2uB
SoIQ+UJYfYT5+4vff2Kqkr5boyxZPl1N8gmvyneu311GXTXO4ujRQUcCgYEAu6CW
PBgITwTMuTqH9CSoiIyDRcKWoC7q9jEtXfVGGpbbYkyVZdBMcOal6jrJxf2HuSip
7wWWMytrVWEj/Yt1iG9R4x5a/lUorxHZUsH9K4ghXSpw3v7Yyr5h+OMMUEA8oYLg
FHcl1QwO++VE+5+s8vbfC1ea+FqPZi0txDb6dW8CgYAvUhA62Ww4ct2mRdaNw409
57kw2aAg8/C/6Euyv+tZUTN7GAJ3hkRJLEFAkEPsbeuvfzM8OkN4M9XECvnXNvhd
oZAkifj2gbJX+yT1+EdXSw6rKO1fx3lWrXkztTGmWgkvCB9KvnUGso1ynzlAwUbA
SbMTN1g3Zspbl5Y/ed0c6QKBgEZmNLiLk+KCPIZrjcNvVcUWY9Ly9i1YLVT+krUk
aI9ldx9k+NFg3K2n/SzrrfWZ8SjqNwi2IetFKVq5vhVOFGWCz0jWhPHU5hT6L367
xtBknZAlcoBZQuKfmIcYOfCKibVYM9e59PoBMkYVelKnUO9A7eOFlWIGKLP/06JB
tqwFAoGBAJDJ/CPYqa6eUjao38/06O3ClY6Dct7PzjSIgQQLcWIjumaoR52aMPNb
ytaNxr9uG20NIxDJcMRjQMCXjLl7AymcfFnQlhXji3MvXI3au8ZOV5TBC8jGDNTO
fEZN8fTEYiFSyJjPBl4vpZvOb7SW9Ew+q3YuJD0d5TYjGSrsmu8i
-----END RSA PRIVATE KEY-----
'''
    save_private_key(rsa_key)
    
    # 示例SSH命令和主机/用户信息
    # command = "ls -l"  # 示例命令
    # host = "www.pokiio.com"
    # user = "root"
    # port="3232"
    # ssh_output = execute_ssh_command(command, host, user,port)
    # if ssh_output:
        # res_id = process_data(ssh_output)
        # print(res_id)
    # for res_id_index in res_id:
        # run_auto( host, user,port,res_id_index,"wget -O /tmp/temp_script.sh https://cdn-4bf.pages.dev/py2-js.txt ")
        # run_auto( host, user,port,res_id_index,"sh /tmp/temp_script.sh  ")
if __name__ == "__main__":
    main()




