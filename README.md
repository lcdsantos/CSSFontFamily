# CSSFontFamily

CSSFontFamily is a Sublime Text 2 plugin with a collection of font stacks autocomplete.

Also, autocomplete @font-faces declared in your current CSS.

## Installation

CSSFontFamily is designed to work with [Sublime Text 2](http://www.sublimetext.com/2).

### Using Sublime Package Control

If you are using [Sublime Package Control](http://wbond.net/sublime_packages/package_control), you can easily install CSSFontFamily via the `Package Control: Install Package` menu item. The CSSFontFamily package is listed as `CSSFontFamily` in the packages list.

### Using Git

Clone this repo directly to your `Packages` directory in the Sublime Text 2 folder.

You can locate your Sublime Text 2 `Packages` directory by using the menu item `Preferences > Browse Packages...`.

While inside the `Packages` directory, clone the plugin repository using the command below:
```git
clone https://github.com/lcdsantos/CSSFontFamily/ "CSSFontFamily"
```

### Download Manually

1. Download the files using the GitHub .zip download option
2. Unzip the files and rename the folder to `CSSFontFamily`
3. Copy the folder to your Sublime Text 2 `Packages` directory

## Usage

The plugin is triggered inside your `font` and `font-family` declarations.

## Customization

The built-in font stacks aren't enough for you? No problem! Go to `Preferences > Package Settings > CSSFontFamily > Settings - User` and add how many you want:
```json
{
	"fonts_stacks": [
		"\"Comic Sans MS\", cursive",
		"\"Your font stack\", sans-serif"
	]
}
```
It's recommended that you escape your font names with quotes if contains spaces or any punctuations other than hyphens.

By default, commented @font-face declarations in your CSS are ignored, you can change this by adding this to your User Settings file:
```json
{
	"ignore_font_faces_in_comments": false
}
```