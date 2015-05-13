import cymysql as mysql # Mysql
import msvcrt as kb # Console I/O
import time, sys, win32gui

'''
CREATE TABLE `track_time` (
	`id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NULL DEFAULT NULL,
	`time` INT(10) UNSIGNED NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `uniq_name` (`name`),
	INDEX `name` (`name`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB;
'''

class Tracker:
	def __init__(self):
		self.connection = mysql.connect(host='localhost', user='root', passwd='', db='money', charset='utf8')
		self.db = self.connection.cursor()

		self.active = self.getActiveWindowTitle()
		self.activeStartTime = time.time()

		self.main()

	def getActiveWindowTitle(self):
		title = win32gui.GetWindowText(win32gui.GetForegroundWindow())
		return unicode(title, "latin-1")

	def saveTimelog(self, title, time):
		self.db.execute("SELECT id FROM track_time WHERE name = %s", title)
		row = self.db.fetchone()

		if row is None:
			self.db.execute("INSERT INTO track_time (name, time) VALUES (%s, %s)", (title, round(time, 1)))
			self.connection.commit()
		else:
			self.db.execute("UPDATE track_time SET time = time + %s WHERE id = %s", (round(time, 1), abs(row[0])))
			self.connection.commit()

	def main(self):
		while(True):
			# Check for exit command, aka q
			if kb.kbhit() and kb.getch() == 'q':
				self.destruct()

			activeWindowTitle = self.getActiveWindowTitle()

			if self.active != activeWindowTitle:
				self.saveTimelog(self.active, time.time() - self.activeStartTime)

				self.active = activeWindowTitle
				self.activeStartTime = time.time()

			time.sleep(0.5)

	def destruct(self):
		# Database cleanup
		self.db.close()
		self.connection.close()

		sys.exit()

if __name__ == '__main__':
	Tracker()
