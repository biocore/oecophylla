def find_local_scratch(in_dir):
    dirlist = in_dir.split('/')
    for i, part in enumerate(dirlist):
        if part.startswith('$'):
            dirlist[i] = os.environ[part[1:]]

    return('/'.join(dirlist))
