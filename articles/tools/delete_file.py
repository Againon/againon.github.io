# 清理文件或目录
import os
import shutil


def delete_drive_files(directory, names):
    # 遍历目录及其子目录
    for root, dirs, files in os.walk(directory):
        # 处理目录
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            # 检查目录是否是需要删除的类型
            # if dir == '.WeDrive' or dir == '.Temp':
            if dir in names:
                try:
                    shutil.rmtree(dir_path)
                    print(f"Deleted directory: {dir_path}")
                except Exception as e:
                    print(f"Failed to delete directory {dir_path}. Reason: {e}")

        # 处理文件
        for file in files:
            # 检查文件是否以.Drive结尾
            # if file.endswith('.Drive'):
            if file in names:
                file_path = os.path.join(root, file)
                try:
                    # 删除文件
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")

# 这里就是清理桌面test目录及子目录下的所有.WeDrive和.Temp文件
directory_to_clean = '/Users/username/Desktop/test'  # 希望被清理的目录路径
names_to_clean = ['.WeDrive', '.Temp']  # 被清理的文件或整个目录名

# #优雅一点
# directory_input = input("请输入清理的目录路径：")
# directory_to_clean = f"{directory_input}"
#
# names_to_clean = [] # names_to_clean = input("请输入你希望被清理的目录名或文件名")
# while True:
#     user_input = input("请输入被清理的目录名或文件名，或输入 'q' 结束: ")
#     if user_input.lower() == 'q':
#         break
#     names_to_clean.append(user_input)
# print("你输入的字符串列表是:", names_to_clean)

delete_drive_files(directory_to_clean, names_to_clean)
