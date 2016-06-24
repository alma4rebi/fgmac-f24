/* -*- mode: js2; js2-basic-offset: 4; indent-tabs-mode: nil -*- */

/* Copyright (c) Chris Vine, 2011 to 2013
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

const Clutter = imports.gi.Clutter;
const St = imports.gi.St;
const GLib = imports.gi.GLib;
const Gio = imports.gi.Gio;

const Main = imports.ui.main;
const PanelMenu = imports.ui.panelMenu;
const PopupMenu = imports.ui.popupMenu;
const AppFavorites = imports.ui.appFavorites;

const ExtensionUtils = imports.misc.extensionUtils

const Mainloop = imports.mainloop;
const Gettext = imports.gettext;

var settings_id = null;
var settings = null;
var button = null;
var menu_actor = null;

// disable() can be called by the system before the timer in enable()
// has fired.  We need to disconnect the timer in disable() where this
// happens
var timer_id = null;


function set_panel_display(button) {
    if (menu_actor) button.actor.remove_actor(menu_actor);

    if (settings.get_boolean("icon")) {
        let fpath = Gio.file_new_for_path(ExtensionUtils.getCurrentExtension().path +
                                          "/emblem-favorite.png");
        let icon = new St.Icon({gicon: new Gio.FileIcon({file: fpath}),
                                style_class: "favorites-icon"});
        button.actor.add_actor(icon);
        menu_actor = icon;
    }
    else {
        let hbox = new St.BoxLayout({style_class: "panel-status-menu-box"});
        hbox.add_child(new St.Label({text: Gettext.gettext("Favorites"),
				     y_expand: true,
				     y_align: Clutter.ActorAlign.CENTER
				    }));
        hbox.add_child(new St.Label({text: "\u25BE",
                                     y_expand: true,
                                     y_align: Clutter.ActorAlign.CENTER
				    }));
        button.actor.add_actor(hbox);
        menu_actor = hbox;
    }
}

function add_item(button, app) {
    let item = new PopupMenu.PopupBaseMenuItem;
    button.menu.addMenuItem(item);
    let box = new St.BoxLayout({vertical: false,
				pack_start: false,
				style_class: "favorites-menu-box"});
    item.actor.add_child(box);
    let icon = app.create_icon_texture(24);
    box.add(icon);
    let label = new St.Label({text: app.get_name()});
    box.add(label);
    item.connect("activate", function () {app.open_new_window(-1);});
}

function build_menu(button) {
    AppFavorites.getAppFavorites().getFavorites().forEach(function (app) {
        add_item(button, app);
    });
}

function get_settings() {
    let schema_id = "org.gnome.shell.extensions.favorites";
    let schema_path = ExtensionUtils.getCurrentExtension().path + "/schemas";
    let schema_source = Gio.SettingsSchemaSource.new_from_directory(schema_path,
								    Gio.SettingsSchemaSource.get_default(),
								    false);
    if (!schema_source) {
        throw new Error("Local schema directory for " + schema_id + " is missing");
    }
    let schema = schema_source.lookup(schema_id, true);
    if (!schema) {
        throw new Error("Schema " + schema_id + " is missing.  Has glib-compile-schemas been called for it?");
    }
    return new Gio.Settings({settings_schema: schema});
}

function enable() {
    // A one-shot timer of 100mS duration so that our panel button is
    // the last to be inserted in the panel's left box.  This is
    // necessary to ensure that the user's chosen position is
    // respected.  This does not give rise to any race condition with
    // respect to the user's actions on the GUI, because until the
    // timeout callback executes the favorites menu cannot be acted on
    // by the user (it is not in the panel and the changed signal has
    // not been connected).
    timer_id = Mainloop.timeout_add(100, function () {
	timer_id = null;
	settings = get_settings();
	button = new PanelMenu.Button(0.0);
	set_panel_display(button);
	build_menu(button);

	settings_id = global.settings.connect("changed::" + AppFavorites.getAppFavorites().FAVORITE_APPS_KEY,
					      function() {
						  button.menu.removeAll();
						  build_menu(button);
					      });

	Main.panel.addToStatusArea("favorites", button, settings.get_int("position") - 1, "left");

	settings.connect("changed::icon", function () {
	    set_panel_display(button);
	});
	settings.connect("changed::position", function () {
	    let pos = settings.get_int("position") - 1;
	   
	    button.destroy();
	    button = new PanelMenu.Button(0.0);
	    set_panel_display(button);
	    build_menu(button);
	    Main.panel.addToStatusArea("favorites", button, pos, "left");
	});
	return false;
    });
}

function disable() {
    if (settings_id) global.settings.disconnect(settings_id);
    if (timer_id) Mainloop.source_remove(timer_id);
    if (button) button.destroy();
    settings_id = null;
    timer_id = null;
    settings = null;
    button = null;
    menu_actor = null;
}

function init() {
    let user_locale_path = ExtensionUtils.getCurrentExtension().path + "/locale";
    Gettext.bindtextdomain("favorites", user_locale_path);
    Gettext.textdomain("favorites");
}
