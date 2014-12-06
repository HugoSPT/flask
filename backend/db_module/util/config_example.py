import ConfigParser

if __name__ == '__main__':
	config = ConfigParser.ConfigParser()
	config.read('../../../config.cfg')

	print config.get('System', 'mongo')
	print config.get('System', 'rabbit')