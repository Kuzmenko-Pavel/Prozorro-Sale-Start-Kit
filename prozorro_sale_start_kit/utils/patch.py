import PyInquirer


def inquirer_control_init_choices(self, choices):
    self.choices = []  # list (name, value)
    searching_first_choice = True if self.pointer_index == 0 else False
    for i, c in enumerate(choices):
        if isinstance(c, PyInquirer.Separator):
            self.choices.append(c)
        else:
            name = c['name']
            value = c.get('value', name)
            disabled = c.get('disabled')
            description = c.get('description', None)
            if c.get('checked') and not disabled:
                self.selected_options.append(value)
            self.choices.append((name, value, disabled, description))
            if searching_first_choice and not disabled:  # find the first (available) choice
                self.pointer_index = i
                searching_first_choice = False


def py_inquirer_patch():
    PyInquirer.prompts.checkbox.InquirerControl._init_choices = inquirer_control_init_choices
