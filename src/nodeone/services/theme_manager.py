class ThemeManager:
    def __init__(self):
        theme_path = "src/nodeone/resources/themes"
        self.themes = {
            "dark": f"{theme_path}/dark.qss",
            "light": f"{theme_path}/light.qss",
        }
        self.current_theme = "dark"

    def apply_theme(self, app, theme_name=None):
        if not theme_name:
            theme_name = self.current_theme
        if theme_name in self.themes:
            with open(self.themes[theme_name], "r") as f:
                app.setStyleSheet(f.read())
            self.current_theme = theme_name
