content = []
with open('kitti_eigen_train_files_with_gt.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        content.append(line)

new_f = open('new_kitti_eigen_train_files_with_gt.txt', 'w')
for i in content:
    if "2011_09_26_drive_0035_sync" in i.split("/")[1]:
        i_list = i.split(" ")
        new_f.write(i_list[0] + " " + i_list[1] + " " + i_list[2] + "\n")
