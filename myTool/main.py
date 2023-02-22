#! /usr/bin/python3
# -*-coding:utf-8-*-

"""
@Time: 2023/2/21 16:13
@Author : mengjie-1998@qq.com
@Remark: a brief description
"""
import re
import subprocess
import time

from BinaryAnalyzer import BinaryAnalyzer


def parserFromAimBytecode(bytecode):
    if len(bytecode) < 1:
        return None

    # 去除 Swarm 哈希
    bytecode = re.sub(r'a165627a7a72305820\S{64}0029$', '', bytecode)

    # 只需要运行时字节码，去除合约创建字节码
    if 'f30060806040' in bytecode:
        bytecode = bytecode[bytecode.index('f30060806040') + 4:]

    return bytecode


def parserFromBytecode(bytecode):
    pass


def parserFromSourceCodeFiles(file, aimContract):
    """
    从源代码文件开始进行解析，适用情形为多个合约写在一个sol文件
    :param file: 输入文件
    :param aimContract: 待检测合约
    """
    # 用 solc 编译合约源代码，获取其二进制代码
    cmd = ['solc', '--bin-runtime', file]
    try:
        binary = subprocess.check_output(cmd).decode()
    except subprocess.CalledProcessError as e:
        print('Compile Error:', file)
        return

    if not binary or len(binary) < 1:
        print('Compile Error:', file)
        return

    tmp = binary.split("\n")

    binaryAnalyzer = BinaryAnalyzer()
    # 遍历 solc 输出的二进制代码字符串列表
    for i in range(len(tmp) - 1):
        # 如果当前字符串是 "Binary"，则该字符串的上一行是合约地址，下一行是合约二进制代码
        if tmp[i].startswith('Binary'):
            name = tmp[i - 1].replace('=', '').replace(' ', '').replace('\n', '')  # 获取合约名称
            bytecode = tmp[i + 1]  # 获取该合约二进制代码
            bytecode = parserFromAimBytecode(bytecode)
            # 如果该合约是我们需要分析的主要合约，则记录结束节点位置
            if aimContract in name:
                pos = binaryAnalyzer.getAimDisasmCode(bytecode) + 1
                binaryAnalyzer.aimContractEndPos = pos
            else:
                binaryAnalyzer.getDisasmCode(bytecode)

    # print(binaryAnalyzer.aimDisasmCode)
    # print(binaryAnalyzer.aimContractEndPos)
    # print(binaryAnalyzer.disasmCode)

    binaryAnalyzer.MCFGConstruction()


def main():
    start_time = time.time()  # 计时开始
    # 从源代码检测缺陷
    file = "1.sol"
    parserFromSourceCodeFiles(file, "Test2")

    end_time = time.time()  # 计时结束
    print(f"Running time: {end_time - start_time:.2f} s")  # 输出总运行时间


if __name__ == '__main__':
    main()