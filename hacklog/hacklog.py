import sys
import ConfigParser
import argparse
import entities
import sqlite3

def main():
	usage = "usage: %prog -c config_file"
	parser=argparse.ArgumentParser()
	parser.add_argument("-c", "--config", dest="config_file",
                      help="configuration file", metavar="FILE")
	options = parser.parse_args()
	if not options.config_file:
		print 'You must specify a config file'
		sys.exit(1)
	config = ConfigParser.ConfigParser()
	config.read(options.config_file)
	if not config.has_option('hacklog', 'test'):
		print 'You must have the test property'
		sys.exit(1)
	test=config.get('hacklog', 'test')
	if not test == "property":
		print 'You must have the right value'
		sys.exit(1)
	print test	
	entities.create_tables()

if __name__ == "__main__":
	main()


