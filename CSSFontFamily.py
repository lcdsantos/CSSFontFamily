import sublime, sublime_plugin
import re

fontFamilies = [
	'Arial, Helvetica, sans-serif',
	'Arial, "Helvetica Neue", Helvetica, sans-serif',
	'"Arial Black", "Arial Bold", Gadget, sans-serif',
	'"Arial Narrow", Arial, sans-serif',
	'"Arial Rounded MT Bold", "Helvetica Rounded", Arial, sans-serif',
	'"Avant Garde", Avantgarde, "Century Gothic", CenturyGothic, "AppleGothic", sans-serif',
	'Calibri, Candara, Segoe, "Segoe UI", Optima, Arial, sans-serif',
	'Candara, Calibri, Segoe, "Segoe UI", Optima, Arial, sans-serif',
	'"Century Gothic", CenturyGothic, AppleGothic, sans-serif',
	'"Franklin Gothic Medium", "Franklin Gothic", "ITC Franklin Gothic", Arial, sans-serif',
	'Futura, "Trebuchet MS", Arial, sans-serif',
	'Geneva, Verdana, "Lucida Sans", "Lucida Grande", "Lucida Sans Unicode", sans-serif',
	'"Gill Sans", "Gill Sans MT", Calibri, sans-serif',
	'"Helvetica Neue", Helvetica, Arial, sans-serif',
	'Impact, Haettenschweiler, "Franklin Gothic Bold", Charcoal, "Helvetica Inserat", "Bitstream Vera Sans Bold", "Arial Black", sans serif',
	'"Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Geneva, Verdana, sans-serif',
	'Optima, Segoe, "Segoe UI", Candara, Calibri, Arial, sans-serif',
	'"Segoe UI", Frutiger, "Frutiger Linotype", "Dejavu Sans", "Helvetica Neue", Arial, sans-serif',
	'Tahoma, Verdana, Segoe, sans-serif',
	'"Trebuchet MS", "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Tahoma, sans-serif',
	'"Trebuchet MS", Arial, Helvetica, sans-serif',
	'"Lucida Sans Unicode", "Lucida Grande", sans-serif',
	'Verdana, Geneva, Tahoma, sans-serif',
	'Baskerville, "Baskerville Old Face", "Hoefler Text", Garamond, "Times New Roman", serif',
	'"Big Caslon", "Book Antiqua", "Palatino Linotype", Georgia, serif',
	'"Bodoni MT", Didot, "Didot LT STD", "Hoefler Text", Garamond, "Times New Roman", serif',
	'"Book Antiqua", Palatino, "Palatino Linotype", "Palatino LT STD", Georgia, serif',
	'"Calisto MT", "Bookman Old Style", Bookman, "Goudy Old Style", Garamond, "Hoefler Text", "Bitstream Charter", Georgia, serif',
	'Cambria, Georgia, Times, "Times New Roman", serif',
	'Didot, "Didot LT STD", "Hoefler Text", Garamond, "Times New Roman", serif',
	'Garamond, Baskerville, "Baskerville Old Face", "Hoefler Text", "Times New Roman", serif',
	'Georgia, Times, "Times New Roman", serif',
	'"Goudy Old Style", Garamond, "Big Caslon", "Times New Roman", serif',
	'"Hoefler Text", "Baskerville old face", Garamond, "Times New Roman", serif',
	'"Lucida Bright", Georgia, serif',
	'Palatino, "Palatino Linotype", "Palatino LT STD", "Book Antiqua", Georgia, serif',
	'Perpetua, Baskerville, "Big Caslon", "Palatino Linotype", Palatino, "URW Palladio L", "Nimbus Roman No9 L", serif',
	'Rockwell, "Courier Bold", Courier, Georgia, Times, "Times New Roman", serif',
	'"Rockwell Extra Bold", "Rockwell Bold", monospace',
	'TimesNewRoman, "Times New Roman", Times, Baskerville, Georgia, serif',
	'"Copperplate Light", "Copperplate Gothic Light", serif',
	'"Andale Mono", AndaleMono, monospace',
	'Consolas, "Lucida Console", Monaco, monospace',
	'"Courier New", Courier, "Lucida Sans Typewriter", "Lucida Typewriter", monospace',
	'"Lucida Console", "Lucida Sans Typewriter", Monaco, "Bitstream Vera Sans Mono", monospace',
	'"Lucida Sans Typewriter", "Lucida Console", Monaco, "Bitstream Vera Sans Mono", monospace',
	'Monaco, Consolas, "Lucida Console", monospace',
	'Copperplate, "Copperplate Gothic Light", fantasy',
	'Papyrus, fantasy'
]

class AutoCompleteFontFamilies(sublime_plugin.EventListener):
	rex = None
	reComments = None
	reFontFace = None

	def on_query_completions(self, view, prefix, locations):
		if not view.match_selector(locations[0], "source.css - meta.selector.css, source.scss - meta.selector.scss, source.css.less"):
			return []

		self.rex = re.compile("(?:font|font\-family):[^;\n}]*$")
		self.reComments = re.compile("\s*(?!<\")\/\*[^\*]+\*\/(?!\")\s*")
		self.reFontFace = re.compile("@font-face\s*\{[\n\t\r\s]*font-family\s*:\s*(?:\'|\")?([^\'\";]+)")

		l = []
		values = list(fontFamilies)
		s = sublime.load_settings("CSSFontFamily.sublime-settings")

		for settingsFontStackItem in s.get('fonts_stacks'):
			if settingsFontStackItem not in fontFamilies:
				values.append(settingsFontStackItem)

		if (view.match_selector(locations[0], "meta.property-value.css, meta.property-value.scss, source.css.less") or
			# This will catch scenarios like .foo {font-style: |}
			view.match_selector(locations[0] - 1, "meta.property-value.css, meta.property-value.scss, source.css.less")):

			loc = locations[0] - len(prefix)
			line = view.substr(sublime.Region(view.line(loc).begin(), loc))
			m = re.search(self.rex, line)

			if m:
				body = view.substr(sublime.Region(0, view.size()))

				if s.get('ignore_font_faces_in_comments'):
					body = re.sub(self.reComments, '', body)

				fontFacesInFile = re.findall(self.reFontFace, body)

				for fontFacesInFileItem in fontFacesInFile:
					if fontFacesInFileItem not in fontFamilies:
						if re.search(r"[^a-zA-Z\-]", fontFacesInFileItem):
							fontFacesInFileItem = "'" + fontFacesInFileItem + "'"

						values.append(fontFacesInFileItem)

				add_semi_colon = view.substr(sublime.Region(locations[0], locations[0] + 1)) != ';'

				for v in values:
					desc = re.sub(r"\"|\'", '', v)
					snippet = v

					if add_semi_colon:
						snippet += ";"

					l.append((desc, snippet))

				return (l, sublime.INHIBIT_WORD_COMPLETIONS)

			return None