// -*- mode: js2; indent-tabs-mode: nil; js2-basic-offset: 4 -*-

/* Copyright (c) Chris Vine, 2012 and 2013
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

const GObject = imports.gi.GObject;
const Gio = imports.gi.Gio;
const Gtk = imports.gi.Gtk;

const ExtensionUtils = imports.misc.extensionUtils;

const Gettext = imports.gettext;


function init() {
    let user_locale_path = ExtensionUtils.getCurrentExtension().path + "/locale";
    Gettext.bindtextdomain("favorites", user_locale_path);
    Gettext.textdomain("favorites");
}

const FavoritesPrefsWidget = new GObject.Class({
    Name: 'Favorites.Prefs.Widget',
    GTypeName: 'FavoritesPrefsWidget',
    Extends: Gtk.Grid,

    _init: function(params) {
	this.parent(params);
        this.margin = 20;
	this.row_spacing = 20;
	this.column_spacing = 10;

	this.attach(new Gtk.Label({label: Gettext.gettext("Panel Icon"),
				   justify: Gtk.Justification.RIGHT,
				   xalign: 1,
				   yalign: 0.5}),
		    0, 0, 1, 1);;
	let alignment = new Gtk.Alignment({xalign: 0,
					   yalign: 0.5,
					   xscale: 0,
					   yscale: 1});
	let icon_check = new Gtk.CheckButton;
	alignment.add(icon_check);
	this.attach(alignment, 1, 0, 1, 1);

	this.attach(new Gtk.Label({label: Gettext.gettext("Panel Position"),
				   justify: Gtk.Justification.RIGHT,
				   xalign: 1,
				   yalign: 0.5}),
		    0, 1, 1, 1);;
	alignment = new Gtk.Alignment({xalign: 0,
				       yalign: 0.5,
				       xscale: 0,
				       yscale: 1});
	let spin = new Gtk.SpinButton;
	spin.set_range(1, 5);
	spin.set_increments(1, 1);
	alignment = new Gtk.Alignment({xalign: 0,
				       yalign: 0.5,
				       xscale: 0,
				       yscale: 1});
	alignment.add(spin);
	this.attach(alignment, 1, 1, 1, 1);

	this._settings = this._get_settings();
	this._settings.bind("icon", icon_check, "active", Gio.SettingsBindFlags.DEFAULT);
	this._settings.bind("position", spin, "value", Gio.SettingsBindFlags.DEFAULT);
    },

    _get_settings: function () {
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
});

function buildPrefsWidget() {
    let widget = new FavoritesPrefsWidget();
    widget.show_all();
    return widget;
}
