import os

# runs setup of base environment and database installs

# create core conda env
environment_yml = '%s/../%s.yml' % (os.__file__, 'environment')
os.call('conda env create --name oecophylla -f %s' % environment_yml)

#TODO change this to os.walk
os.call('find oecophylla -name "*.sh" -execdir bash {} \;')
