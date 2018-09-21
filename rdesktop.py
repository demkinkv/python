#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  rdesktop-gui
#

import configparser
import os
import subprocess
import sys
import urllib.parse

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

os.EX__BASE = 64

def find_rdesktop():
	for directory in os.getenv('PATH').split(':'):
		location = os.path.join(directory, 'rdesktop')
		if os.path.isfile(location):
			return location
	return None

class RdesktopWindow(Gtk.Window):
	def __init__(self, rdesktop_bin, config_path):
		Gtk.Window.__init__(self)
		self.set_title('RDesktop')
		self.set_size_request(300, 250)
		self.set_resizable(False)
		self.set_position(Gtk.WindowPosition.CENTER)
		self.rdesktop_bin = rdesktop_bin
		self.config_path = config_path

		self.config = configparser.ConfigParser()
		self.config.readfp(open(config_path, 'r'))
		if not self.config.has_section('main'):
			self.config.add_section('main')

		main_vbox = Gtk.Box(spacing=7)
		main_vbox.set_property('orientation', Gtk.Orientation.VERTICAL)
		self.add(main_vbox)

		frame = Gtk.Frame()
		frame.set_label('Параметры подключения')
		frame.set_border_width(7)
		main_vbox.add(frame)

		grid = Gtk.Grid()
		grid.set_property('margin-left', 10)
		grid.set_property('margin-right', 10)
		grid.set_property('margin-top', 5)
		grid.set_property('margin-bottom', 7)
		grid.set_property('expand', True)
		grid.set_column_homogeneous(False)
		grid.set_column_spacing(10)
		grid.set_row_homogeneous(True)
		grid.set_row_spacing(7)
		frame.add(grid)

		grid.attach(Gtk.Label('Host'), 1, 1, 1, 1)
		self.host_entry = Gtk.ComboBoxText.new_with_entry()
		self.host_entry.set_property('expand', True)
		if self.config.has_option('main', 'hosts'):
			hosts = self.config.get('main', 'hosts')
			hosts = hosts.split(',')
			for host in hosts[:5]:
				self.host_entry.append_text(host)
			self.host_entry.set_active(0)
		grid.attach(self.host_entry, 2, 1, 1, 1)

		grid.attach(Gtk.Label('Username'), 1, 2, 1, 1)
		self.username_entry = Gtk.Entry()
		self.username_entry.set_property('expand', True)
		if self.config.has_option('main', 'username'):
			self.username_entry.set_text(self.config.get('main', 'username'))
		grid.attach(self.username_entry, 2, 2, 1, 1)
		
		grid.attach(Gtk.Label('Domain'), 1, 3, 1, 1)
		self.domain_entry = Gtk.Entry()
		self.domain_entry.set_property('expand', True)
		if self.config.has_option('main', 'domain'):
			self.domain_entry.set_text(self.config.get('main', 'domain'))
		grid.attach(self.domain_entry, 2, 3, 1, 1)
		
		grid.attach(Gtk.Label('Password'), 1, 4, 1, 1)
		self.password_entry = Gtk.Entry()
		self.password_entry.set_property('expand', True)
		self.password_entry.set_property('visibility', False)
		grid.attach(self.password_entry, 2, 4, 1, 1)

		grid.attach(Gtk.Label('Разрешение'), 1, 5, 1, 1)
		self.geometry_combo = Gtk.ComboBoxText()
		self.geometry_combo.set_property('expand', True)
		self.geometry_combo.append_text('800x600')
		self.geometry_combo.append_text('1024x768')
		self.geometry_combo.append_text('1280x720')
		self.geometry_combo.append_text('1280x960')
		self.geometry_combo.append_text('1366x768')
		self.geometry_combo.append_text('1440x1080')
		self.geometry_combo.append_text('1600x900')
		self.geometry_combo.append_text('1920x1080')
		self.geometry_combo.append_text('[full-screen]')
		self.geometry_combo.set_active(0)
		if self.config.has_option('main', 'geometry'):
			desired_geometry = self.config.get('main', 'geometry')
			idx = 0
			for row in self.geometry_combo.get_model():
				if row[0] == desired_geometry:
					self.geometry_combo.set_active(idx)
					break
				idx += 1
		grid.attach(self.geometry_combo, 2, 5, 1, 1)


		grid.attach(Gtk.Label('RMedia'), 1, 6, 1, 1)
		self.media_combo = Gtk.ComboBoxText()
		self.media_combo.set_property('expand', True)
		self.media_combo.append_text('remote')
		self.media_combo.append_text('local')
		self.media_combo.set_active(0)
		if self.config.has_option('main', 'media'):
			desired_media = self.config.get('main', 'media')
			idx = 0
			for row in self.media_combo.get_model():
				if row[0] == desired_geometry:
					self.media_combo.set_active(idx)
					break
				idx += 1
		grid.attach(self.media_combo, 2, 6, 1, 1)

		grid.attach(Gtk.Label('Shara'), 1, 7, 1, 1)
		self.shara_entry = Gtk.Entry()
		self.shara_entry.set_property('expand', True)
		if self.config.has_option('main', 'shara'):
			self.shara_entry.set_text(self.config.get('main', 'shara'))
		grid.attach(self.shara_entry, 2, 7, 1, 1)

		self.attach_to_console_btn = Gtk.CheckButton(label='Attach To Console')
		if self.config.has_option('main', 'console'):
			attach_to_console = self.config.getboolean('main', 'console')
			self.attach_to_console_btn.set_property('active', attach_to_console)
		grid.attach(self.attach_to_console_btn, 2, 8, 1, 1)

		hbox = Gtk.Box(False)
		hbox.set_property('margin-bottom', 11)
		hbox.set_property('orientation', Gtk.Orientation.HORIZONTAL)
		main_vbox.add(hbox)
		connect_button = Gtk.Button()
		self.connect_button = connect_button
		self.password_entry.connect('activate', lambda w: self.connect_button.emit('clicked'))
		hbox.pack_end(connect_button, False, False, 5)
		hbox = Gtk.Box()
		hbox.set_property('orientation', Gtk.Orientation.HORIZONTAL)
		hbox.add(Gtk.Image.new_from_stock(Gtk.STOCK_APPLY, Gtk.IconSize.BUTTON))
		hbox.add(Gtk.Label('Connect'))
		connect_button.add(hbox)
		connect_button.connect('clicked', self.on_connect_clicked)

	def on_connect_clicked(self, widget):
		execl_args = [self.rdesktop_bin]		
	
		username = self.username_entry.get_text()	
		if username:
			execl_args.append('-u')
			execl_args.append(username)
			self.config.set('main', 'username', username)

		domain = self.domain_entry.get_text()
		if domain:
			execl_args.append('-d')
			execl_args.append(domain)
			self.config.set('main', 'domain', domain)	

		password = self.password_entry.get_text()
		if password:
			execl_args.append('-p')
			execl_args.append(password)

		geometry = self.geometry_combo.get_active_text()
		self.config.set('main', 'geometry', geometry)
		if geometry == '[full-screen]':
			execl_args.append('-f')
		else:
			execl_args.append('-g')
			execl_args.append(geometry)

		media = self.media_combo.get_active_text()
		self.config.set('main', 'media', media)
		if media:
			execl_args.append('-r')						
			execl_args.append('sound:'+media)

		shara = self.shara_entry.get_text()
		if shara:
			execl_args.append('-r')
			execl_args.append('disk:tmp='+shara)
			self.config.set('main', 'shara', shara)

		attach_to_console = self.attach_to_console_btn.get_active()
		if attach_to_console:
			execl_args.append('-0')
		self.config.set('main', 'console', str(attach_to_console))

		host = self.host_entry.get_active_text()
		if self.config.has_option('main', 'hosts'):
			hosts = self.config.get('main', 'hosts').split(',')
			hosts = [h for h in hosts if h != host]
			hosts.insert(0, host)
			hosts = hosts[:5]
			self.config.set('main', 'hosts', ','.join(hosts))
		else:
			self.config.set('main', 'hosts', host)
		execl_args.append(host)
		self.config.write(open(self.config_path, 'w'))

		self.hide()
		while Gtk.events_pending():
			Gtk.main_iteration()
		proc_h = subprocess.Popen(execl_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		result = proc_h.wait()
		if result < os.EX__BASE:
			Gtk.main_quit()
			return
		self.show_all()
		error_dialog = Gtk.MessageDialog(self, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, 'An Error Occurred')
		error_dialog.set_title('Error')
		error_dialog.run()
		error_dialog.destroy()
		return

def main():
	rdesktop_bin = find_rdesktop()
	if not rdesktop_bin:
		print('could not locate the rdesktop binary')
		print('install it and try again')
		return 0
	config_path = os.path.join(os.path.expanduser('~'), '.config', 'rdesktop-gui.conf')
	if not os.path.isfile(config_path):
		open(config_path, 'w')
	win = RdesktopWindow(rdesktop_bin, config_path)
	win.connect('delete-event', Gtk.main_quit)
	if len(sys.argv) > 1:
		connection_information = urllib.parse.urlparse(sys.argv[1])
		if connection_information.scheme in ['rdp', 'mstsc']:
			win.host_entry.prepend_text(connection_information.hostname or '')
			win.host_entry.set_active(0)
			win.username_entry.set_text(connection_information.username or '')
			win.password_entry.set_text(connection_information.password or '')
	win.show_all()
	Gtk.main()

if __name__ == '__main__':
	main()
