import os
import re



def search_file():
    for (path, dir, files) in os.walk("/mnt/c/Users/NHNEnt/Documents/Project/salt/public-gwiyeong-salt/salt/tgt"):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.py':
                yield (path, filename)

def find_def_make_file(path, file):
    func_name_re = r'def ([\w]*)'
    f_list = []
    with open('{}/{}'.format(path, file), 'r') as f:
        if file == '__init__.py':
            dir_name = './'
        else:
            dir_name = './{}/'.format(file.split('.')[0])

        if not os.path.isdir(dir_name):
            os.mkdir(dir_name, 0755)

        for line in f.readlines():
            if line.startswith('def'):
                func_name = re.search(func_name_re, line).group(1)
                print(func_name)
                if os.path.isfile(dir_name + func_name + '.py'):
                    f_list.append(open(dir_name + func_name + '.py.1', 'w'))
                else:
                    f_list.append(open(dir_name + func_name + '.py', 'w'))
                f_list[len(f_list) - 1].write(line)
            elif line.strip().startswith('class'):
                pass
            else:
                if len(f_list) != 0:
                    f_list[len(f_list) - 1].write(line)

    for ff in f_list:
        ff.close()


if __name__ == "__main__":
    for path, file in search_file():
        find_def_make_file(path, file)
  
