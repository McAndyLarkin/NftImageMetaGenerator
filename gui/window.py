import random
from tkinter import *
from tkinter import filedialog

from gui.repository import *
from image_combinations import ImageCombinator
from threading import Thread


class Screen:
    class Modes:
        cloud_tab = "Cloud"
        new_gen_tab = "New gen"
        update_meta = "Update meta"

        @staticmethod
        def list():
            return [Screen.Modes.new_gen_tab, Screen.Modes.cloud_tab, Screen.Modes.update_meta]

        tabs = []

    meta_entities: dict = {}
    destiny: str = None
    name: str = None
    source: str = None
    count: int = None
    cloud_path: str = None

    meta_file: str = None
    meta_directory: str = None
    meta_target: str = "File|Dir"

    tab_mode: str = None

    @staticmethod
    def updateMessage(message):
        pass

    onScreenModeUpdated = []

    @staticmethod
    def updateScreenMode(mode):
        print("updateScreenMode", mode)
        for i in Screen.onScreenModeUpdated:
            i(mode)


    @staticmethod
    def hide_or_show_launch_buts(show: bool):
        pass

dark_back = "#262626"
light_back = "#dbdbdb"
green = "#62c47c"
yellow = "#dbb948"


def launchWindow():
    print("Init Window")
    initWindow()


def getPath(search="File|Dir", filetypes=None):
    path = ""
    if search == "File":
        if filetypes is None:
            filetypes = [("All files", "*.*")]

        path = filedialog.askopenfilename(
            title='Open a file',
            initialdir='~/',
            filetypes=filetypes)
    elif search == "Dir":
        path = filedialog.askdirectory(
            title='Select path',
            initialdir='~/')
    if path == "":
        return None
    else:
        return path


def setText(field, text, cut_length):
    if text is not None:
        text = "..." + ''.join(reversed(text[-1:-cut_length:-1]))
        if type(field) == Entry:
            field.delete(0, 'end')
            field.insert(0, text)
        elif type(field) == Label:
            field["text"] = text


def createPathRaw(root, name, command, search="File|Dir", filetypes=None, color_mode="white|black", default=None):
    frame = Frame(root)

    aspect1 = .26
    aspect2 = .66

    if color_mode == "black":
        title = Label(frame, text=name + ": ", bg=dark_back, fg="white")
        fk = "black"
    else:
        title = Label(frame, text=name + ": ", bg=light_back, fg="black")
        fk = "black"

    title.place(relx=0, rely=0, relwidth=aspect1, relheight=1)
    title.config(font=("Courier", 12))

    field = Label(frame, bg=light_back, fg=fk, highlightcolor=light_back)
    field.place(relx=aspect1, rely=0, relheight=.8, relwidth=aspect2)
    field.config(font=("Courier", 12))


    def f(path):
        if command(path):
            setText(field, path, 40)
        else:
            setText(field, "", 0)

    find_btn = Button(frame, text=search,
                      command=(lambda: f(getPath(search, filetypes)))
                      )
    find_btn.place(relx=aspect1 + aspect2, rely=0, relheight=1, relwidth=1 - aspect1 - aspect2)

    if default is not None:
            setText(field, default, 40)

    return frame


def createMetaRaw(root, name, command, color_mode="white|black", default=None, long=False):
    """

    :param command:
    :param root:
    :param name: json path as "root/root2/key" or just "key
    :return:
    """
    frame = Frame(root, bg=light_back)

    if long:
        aspect = .45
    else:
        aspect = .25

    if color_mode == "black":
        bg = dark_back
        fg = "white"
    else:
        bg = light_back
        fg = "black"

    title = Label(frame, text=name + ": ", bg=bg, fg=fg)

    title.place(relx=0, rely=0, relwidth=aspect, relheight=1)
    title.config(font=("Courier", 12))

    field = Entry(frame, bg=light_back, fg="black")
    sv = StringVar()

    def f(sv):
        if not command(name, sv.get()):
            field.delete(0, END)

    sv.trace("w", lambda __, _, ___, sv=sv: f(sv))

    field.place(relx=aspect, rely=0, relheight=1, relwidth=1 - aspect)
    field.config(font=("Courier", 12), textvariable=sv)

    if default is not None:
        field.insert(0, default)

    return frame


def getMetaFields():
    return ["name",
            "description",
            "ipfs(image)",
            "seller_fee_basis_points",
            "external_url",
            "collection/name",
            "collection/family",
            "properties/creators/address",
            "properties/creators/share",
            "compiler"
            ]


def initMetaFragment(root):
    frame = Frame(root, bg=light_back)
    frame.place(relwidth=.48, relheight=.98, relx=.01, rely=.01)

    title = Label(frame, text="META", font=50, bg=light_back)
    title.config(font=("Courier", 16), fg="black")
    title.pack()

    names = getMetaFields()
    field_relheight = 20

    def f(name, value):
        if name is not None and value is not None and \
                not len(value) == 0 and not len(name) == 0:
            Screen.meta_entities[name] = value
            return True
        elif name is not None and not len(name) == 0:
            Screen.meta_entities.pop(name)
            return False

    for name_i in range(len(names)):
        name = names[name_i]
        if Screen.meta_entities.__contains__(name):
            default = Screen.meta_entities[name]
        else:
            default = None
        field1 = createMetaRaw(frame, name, color_mode="white", command=f, default=default, long=True)
        field1.place(relwidth=.98, height=field_relheight, relx=.01, y=field_relheight * (name_i + 1))


def initGeneralFragment(root):
    frame = Frame(root, bg=dark_back)
    frame.place(relwidth=.48, relheight=.4, rely=.7, relx=.51)

    field_relheight = 25

    def f_name(__, name):
        if name is not None and not len(name) == 0:
            Screen.name = name
            return True
        else:
            Screen.name = None
            return False

    name_field = createMetaRaw(frame, "Name", color_mode="black", command=f_name, default=Screen.name)
    name_field.place(height=field_relheight, relwidth=.98, relx=.01, y=field_relheight)

    def f_path(path):
        if path is not None and not len(path) == 0:
            Screen.destiny = path
        return True

    destiny_field = createPathRaw(frame, command=(lambda p: f_path(p)), name="Destiny", search="Dir",
                                  color_mode="black", default=Screen.destiny)
    destiny_field.place(height=field_relheight, relwidth=.98, relx=.01, y=field_relheight * 2)

    calc_gen__btn = Button(frame, text="Calculate&Generate", highlightbackground=dark_back,
                           command=calc_or_gen_or_update_btn, fg=green)
    calc_gen__btn.place(height=50, relwidth=.3, relx=.01, y=field_relheight * 5)

    calc_btn = Button(frame, text="Calculate", highlightbackground=dark_back, command=calculate_btn, fg=yellow)

    calc_btn.place(height=50, relwidth=.2, relx=.01, y=field_relheight * 7)

    def hide_or_show(show: bool):
        if show:
            calc_gen__btn.config(state=NORMAL)
            if Screen.tab_mode == Screen.Modes.new_gen_tab:
                calc_btn.config(state=NORMAL)
        else:
            calc_gen__btn.config(state=DISABLED)
            calc_btn.config(state=DISABLED)

    Screen.hide_or_show_launch_buts = hide_or_show

    def f_update(screenMode):
        Screen.tab_mode = screenMode
        if screenMode == Screen.Modes.cloud_tab:
            calc_gen__btn["text"] = "Generate"
            calc_gen__btn.config(state=NORMAL)
            calc_btn.config(state=DISABLED)
            name_field.place(height=field_relheight, relwidth=.98, relx=.01, y=field_relheight)
            destiny_field.place(height=field_relheight, relwidth=.98, relx=.01, y=field_relheight * 2)
        elif screenMode == Screen.Modes.new_gen_tab:
            calc_gen__btn["text"] = "Calculate&Generate"
            calc_gen__btn.config(state=NORMAL)
            calc_btn.config(state=NORMAL)
            name_field.place(height=field_relheight, relwidth=.98, relx=.01, y=field_relheight)
            destiny_field.place(height=field_relheight, relwidth=.98, relx=.01, y=field_relheight * 2)
        elif screenMode == Screen.Modes.update_meta:
            calc_gen__btn["text"] = "Update Metadata"
            calc_gen__btn.config(state=NORMAL)
            calc_btn.config(state=DISABLED)
            name_field.place_forget()
            destiny_field.place_forget()


    f_update(Screen.tab_mode)

    Screen.onScreenModeUpdated.append(f_update)

    mode_description = Label(frame, text="Check data entered\nbefore start generating", anchor="w", justify=LEFT,
                             background=dark_back, foreground=light_back)

    def f_message(message):
        mode_description["text"] = message

    Screen.updateMessage = f_message
    mode_description.place(relheight=.40, relwidth=.48, relx=.42, y=field_relheight * 4)
    mode_description.config(font=("Courier", 10))


def check_for_calculating():
    print("check_for_calculating ..")
    missed_fields = []

    if Screen.tab_mode == Screen.Modes.cloud_tab or Screen.tab_mode == Screen.Modes.update_meta:
        return {
            "result": False,
            "Err": "WRONG_MODE"
        }

    if Screen.destiny is None:
        print("Destiny is null")
        missed_fields.append("Destiny")
    else:
        print("Destiny: " + Screen.destiny)

    if Screen.name is None:
        print("Name is null")
        missed_fields.append("Project Name")
    else:
        print("Name: " + Screen.name)

    if Screen.source is None:
        print("Source is null")
        missed_fields.append("Source path")
    else:
        print("Source: " + Screen.source)

    if Screen.count is None:
        print("Count is null")
        missed_fields.append("Count")
    else:
        print("Count: " + str(Screen.count))

    if len(missed_fields) != 0:
        return {
            "result": False,
            "Err": "MISSED_FIELDS",
            "fields": missed_fields
        }
    return {
            "result": True
        }


def check_for_generating():
    print("check_for_generating ..", Screen.tab_mode)

    if Screen.tab_mode == Screen.Modes.new_gen_tab:
        return {
            "result": True
        }
    elif Screen.tab_mode != Screen.Modes.cloud_tab:
        return {
            "result": False,
            "Err": "WRONG_MODE"
        }

    missed_fields = []
    if Screen.destiny is None:
        print("Destiny is null")
        missed_fields.append("Destiny")
    else:
        print("Destiny: " + Screen.destiny)

    if Screen.name is None:
        print("Name is null")
        missed_fields.append("Project Name")
    else:
        print("Name: " + Screen.name)

    if Screen.tab_mode != Screen.Modes.cloud_tab:
        return {
            "result": False,
            "Err": "WRONG_MODE"
        }

    if Screen.cloud_path is None:
        print("Cloud path is null")
        missed_fields.append("Cloud path")
    else:
        print("Cloud path: " + Screen.cloud_path)

    if len(missed_fields) != 0:
        return {
            "result": False,
            "Err": "MISSED_FIELDS",
            "fields": missed_fields
        }
    return {
            "result": True
        }


def calculate(args):
    update = args
    if not os.path.exists(Screen.source):
        update("Calculating is Impossible \n There is not source")
        return
    update("Calculating ...")

    psd_file_name = Screen.source
    print("Calculating .. ", psd_file_name)
    combinator = ImageCombinator(psd_file_name)

    top = combinator.getTopGroups()

    print("Groups:", *top, sep='\n', end="\n\n")

    print("All layers -- ", *combinator.getAllLayers(), sep="\n", end="\n\n")

    combinator.setCombinable([i[0] for i in top])

    combinations = combinator.getCombinations(Screen.count, update)
    print("Result of calculating:", len(combinations[0]), combinations[1], combinations[2])

    combinations = sorted(combinations[0], key=lambda _: random.random()), combinations[1], combinations[2]
    file_name = combinator.save_cloud(combinations[0], configure={
        "Source": Screen.source,
        "GenName": Screen.name
    }, path=Screen.destiny)

    Screen.updateMessage("Calculating has been finished:\n"
                         "You can find your cloud file\n{}\n"
                         "in {}".format(os.path.basename(file_name), Screen.destiny))
    if len(combinations[0]) == 0:
        return None

    return combinations


def calculate_btn():
    if Screen.tab_mode != Screen.Modes.new_gen_tab:
        return {
            "result": False,
            "Err": "WRONG_MODE"
        }
    print("check_for_calculating ..")
    checking = check_for_calculating()
    if checking['result']:
        print("Success!")
        Screen.updateMessage("Calculating ...")

        def target():
            calculate(Screen.updateMessage)
            Screen.hide_or_show_launch_buts(True)
        th = Thread(target=target)
        th.start()
    else:
        print("Failed(")
        if checking['Err'] == "MISSED_FIELDS":
            print("Missed", *checking['fields'])
            Screen.updateMessage("You have not filled \nnecessary fields: \n{}".format(checking['fields']))
        if checking['Err'] == "WRONG_MODE":
            print("WRONG_MODE")
            Screen.updateMessage("Select 'New Gen' tab to configure new generation")
        else:
            print("Unknown calculating error")
            Screen.updateMessage("Unknown error.\nClose app and try again")


def update_metadate():
    print("mEta", Screen.meta_file)
    update_meta_file(Screen.meta_entities, Screen.meta_file, Screen.updateMessage)


def calc_or_gen_or_update_btn():
    print("calculate_and_generate .. ")
    checking = None

    if Screen.tab_mode == Screen.Modes.update_meta:
        update_metadate()
        return

    if Screen.tab_mode == Screen.Modes.new_gen_tab:
        checking = check_for_calculating()
        if checking['result']:
            print("Success!")
            checking = check_for_generating()

    elif Screen.tab_mode == Screen.Modes.cloud_tab:
        checking = check_for_generating()

    if checking is None:
        Screen.updateMessage("Unknown error.\nClose app and try again")

    if checking['result']:
        print("Success!")
        if Screen.tab_mode == Screen.Modes.new_gen_tab:
            class MyThread(Thread):
                def __init__(self, parent=None):
                    self.parent = parent
                    super(MyThread, self).__init__()
                def run(self):
                    Screen.hide_or_show_launch_buts(False)
                    combinations = calculate(Screen.updateMessage)
                    if combinations is None:
                        print("Failed to start generating: Combinations")
                        Screen.updateMessage("Generating is impossible.\nThere is not combinations")
                    else:
                        generate(combinations, Screen.source, Screen.updateMessage)
                    Screen.hide_or_show_launch_buts(True)

            thread = MyThread()
            thread.start()

        elif Screen.tab_mode == Screen.Modes.cloud_tab:
            print("Cloud loading..")
            Screen.updateMessage("Cloud loading ...")
            source = get_cloud_content(Screen.cloud_path, Screen.updateMessage)
            if source is not None:
                source = source["Source"]
            combinations = get_cloud_combinations(Screen.cloud_path, print)

            if source is None:
                print("Failed to start generating: Source")
                Screen.updateMessage("Generating is impossible.\nThere is not source file")
            elif combinations is None:
                print("Failed to start generating: Combinations")
                Screen.updateMessage("Generating is impossible.\nThere is not combinations")
            else:
                def target():
                    generate(combinations, source, Screen.updateMessage)
                    Screen.hide_or_show_launch_buts(True)
                th = Thread(target=target)
                Screen.hide_or_show_launch_buts(False)
                th.start()

    else:
        print("Failed(")
        if checking['Err'] == "MISSED_FIELDS":
            print("Missed", *checking['fields'])
            Screen.updateMessage("You have not filled \nnecessary fields: \n{}".format(checking['fields']))
        if checking['Err'] == "WRONG_MODE":
            print("WRONG_MODE")
            Screen.updateMessage("Unknown mode")
        else:
            print("Unknown error")
            Screen.updateMessage("Unknown error.\nClose app and try again")


def generate(combinations, source, updateMsg):
    if source is None or not os.path.exists(source):
        updateMsg("Generating is unavailable \nbecause there is not source")
        return
    elif combinations is None:
        updateMsg("Generating is unavailable \nbecause there is not combinations")
        return
    elif Screen.name is None:
        updateMsg("Generating is unavailable \nbecause there is not name")
        return

    updateMsg("Generating...")
    combinations, restored_part, part_of_all = combinations
    print("Generating: combos.len -- {}, restored_part -- {}, part_of_all -- {}"
          .format(combinations, restored_part, part_of_all))

    export_name = get_project_file_name(content={
        "Source": source,
        "Generation": Screen.name,
        "Count": len(combinations)
    })
    path = Screen.destiny + '/' + export_name + '/'
    print("generating destiny path -- ", path)

    combinator = ImageCombinator(source)
    print(Screen.meta_entities)
    combinator.generateImages(combinations=combinations, image_template=Screen.name + '#',
                                  path=path, exp="png",
                              maximum=len(combinations), meta=Screen.meta_entities, updateMsg=updateMsg)
    updateMsg("Generating has been finished:\n"
                         "You can find your generated images and meta in \n{}"
                         .format(path))


def initCloudTable(root):
    print("cloud_path", Screen.cloud_path)
    h = Scrollbar(root, orient='horizontal')
    h.pack(side=BOTTOM, fill=X)

    v = Scrollbar(root)
    v.pack(side=RIGHT, fill=Y)

    content = Text(root, wrap=NONE,
                   xscrollcommand=h.set,
                   yscrollcommand=v.set, font=("Courier", 14))
    content.place(x=.01, y=0.01, relwidth=0.98, relheight=0.98)

    lines = get_cloud_content(Screen.cloud_path, error_handling=show_message)
    t2 = '  '
    t4 = '    '
    if lines is not None:
        for key, value in lines.items():
            if type(value) == dict:
                content.insert(END, key + ': ' + "\n")
                for v_key, v_value in value.items():
                    content.insert(END, t2 + v_key + ': ' + "\n")
                    if type(v_value) == dict:
                        for v_v_key, v_v_value in v_value.items():
                            content.insert(END, t4 + v_v_key + ': ' + v_v_value + "\n")
                    elif type(v_value) == str:
                        content.insert(END, t2 + v_key + ': ' + v_value + "\n")

            elif type(value) == str:
                content.insert(END, key + ': ' + value + "\n")
    else:
        content.insert(END, "Cloud hasn't been loaded")
    content.config(state=DISABLED)

    h.config(command=content.xview)
    v.config(command=content.yview)


def initCloudFragment(root):
    frame = Frame(root, bg=light_back)
    place_mode_screen(frame)

    title_height = 25
    spacer = 20

    title = Label(frame, text="Load from Cloud", bg=light_back, fg="black")
    title.place(relx=0, y=5, height=title_height, relwidth=1)
    title.config(font=("Courier", 18))

    table = Frame(frame, bg=dark_back)
    table.place(relx=.01, relwidth=.8, y=title_height + spacer, height=400)
    initCloudTable(table)

    def open_cloud(path):
        if path is not None and not len(path) == 0:
            Screen.cloud_path = path
            for widget in table.winfo_children():
                widget.destroy()
            initCloudTable(table)
        return True

    open_f = createPathRaw(root, "Open cloud", command=open_cloud, search="File",
                           filetypes=[("Cloud files", "*.ccld")], color_mode="white", default=Screen.cloud_path)
    open_f.place(rely=0.85, relx=0.01, height=20, relwidth=.98)

    return frame

def initUpdateMetaFrgment(root):
    frame = Frame(root, bg=dark_back)
    place_mode_screen(frame)

    title = Label(frame, text="Update metadata", bg=dark_back, fg="white")
    title.place(relx=0, y=5, height=20, relwidth=1)
    title.config(font=("Courier", 18))

    title2 = Label(frame, text="Select 1 file or directory with files", bg=dark_back, fg="white")
    title2.place(relx=0, y=25, height=20, relwidth=1)
    title2.config(font=("Courier", 14))

    def select_file(path):
        if path is not None and not len(path) == 0:
            Screen.meta_file = path
            return True
        return  False

    def select_directory(path):
        if path is not None and not len(path) == 0:
            Screen.meta_directory = path
            return True
        return  False

    open_f = createPathRaw(frame, "Meta file", command=select_file, search="File",
                           filetypes=[("JSON files", "*.json")], color_mode="black", default=Screen.meta_file)

    open_d = createPathRaw(frame, "Meta folder", command=select_directory, search="Dir",
                           filetypes=None, color_mode="black", default=Screen.meta_directory)

    var1 = StringVar()
    var1.set("File")

    def show():
        Screen.meta_target = var1.get()
        if var1.get() == "Dir":
            open_f.place_forget()
            open_d.place(y=90, relx=0.01, height=20, relwidth=.98)
        elif var1.get() == "File":
            open_d.place_forget()
            open_f.place(y=90, relx=0.01, height=20, relwidth=.98)
        else:
            open_d.place_forget()
            open_f.place_forget()

    c1 = Radiobutton(frame, text="File",
                     variable=var1,
                     value="File",
                     command=show)

    c2 = Radiobutton(frame, text="Dir",
                     variable=var1,
                     value="Dir",
                     command=show)

    c1.place(y=55, relx=0.01, height=20, width=50)
    c2.place(y=55, relx=0.16, height=20, width=50)

    show()
    return frame


def initNewGenFragment(root):
    frame = Frame(root, bg=dark_back)
    place_mode_screen(frame)

    title = Label(frame, text="Create new Generation", bg=dark_back, fg="white")
    title.place(relx=0, y=5, height=20, relwidth=1)
    title.config(font=("Courier", 18))

    def open_source(path):
        if path is not None and not len(path) == 0:
            Screen.source = path
        return True

    open_f = createPathRaw(frame, "Open source", command=open_source, search="File",
                           filetypes=[("Photoshop files", "*.psd")], color_mode="black", default=Screen.source)
    open_f.place(rely=0.1, relx=0.01, height=20, relwidth=.98)

    def f_count(__, count: str):
        if count is not None and count.isnumeric():
            Screen.count = int(count)
            return True
        else:
            Screen.count = None
            return False

    name_field = createMetaRaw(frame, "Count", color_mode="black", command=f_count, default=Screen.count)
    name_field.place(height=20, relwidth=.98, relx=.01, rely=.1, y=25)

    return frame


def initTabsFragment(root, tabs):
    frame = Frame(root, bg=light_back)
    frame.place(height=20, relwidth=1)

    for tab_i in range(len(tabs)):
        Screen.Modes.tabs.append(createTab(frame, Screen.Modes.list()[tab_i], tab_i=tab_i))


def createTab(root, name, tab_i):
    tab_btn = Button(root, font=30, text=name,
                     highlightbackground=dark_back)

    tab_btn.place(relx=(tab_i) * (1 / len(Screen.Modes.list())), height=20, relwidth=1 / len(Screen.Modes.list()))
    tab_btn.config(font=("Courier", 10))
    tab_btn.config(command=lambda: Screen.updateScreenMode(name))
    onTabSelectedUnselected(tab_btn)
    return tab_btn


def onTabSelectedUnselected(tab):
    if tab["text"] == Screen.tab_mode:
        tab.config(fg=green)
    else:
        tab.config(fg=dark_back)


def initOptionFragment(root):
    frame = Frame(root, bg=light_back)
    frame.place(relwidth=.48, relheight=.7, rely=.01, relx=.51)

    cloud: Frame = initCloudFragment(frame)
    newGen: Frame = initNewGenFragment(frame)
    updateMeta: Frame = initUpdateMetaFrgment(frame)

    Screen.tab_mode = Screen.Modes.new_gen_tab

    def f_update(screenMode):
        Screen.tab_mode = screenMode
        if screenMode == Screen.Modes.cloud_tab:
            newGen.place_forget()
            updateMeta.place_forget()
            place_mode_screen(cloud)
        elif screenMode == Screen.Modes.new_gen_tab:
            cloud.place_forget()
            updateMeta.place_forget()
            place_mode_screen(newGen)
        elif screenMode == Screen.Modes.update_meta:
            newGen.place_forget()
            cloud.place_forget()
            place_mode_screen(updateMeta)

        for _tab in Screen.Modes.tabs:
            onTabSelectedUnselected(_tab)

    f_update(Screen.tab_mode)

    Screen.onScreenModeUpdated.append(f_update)

    initTabsFragment(frame, tabs=Screen.Modes.list())


def place_mode_screen(frame):
    frame.place(y=20, relheight=1, relwidth=1)


def build_config():
    return {
            "meta_entities": Screen.meta_entities,
            "destiny": Screen.destiny,
            "name": Screen.name,
            "source": Screen.source,
            "count": Screen.count,
            "cloud_path": Screen.cloud_path,
            "meta_file": Screen.meta_file,
            "meta_dir": Screen.meta_directory
        }


def apply_config(config):
    Screen.meta_entities = config["meta_entities"]
    Screen.destiny = config["destiny"]
    Screen.name = config["name"]
    Screen.source = config["source"]
    Screen.count = config["count"]
    Screen.cloud_path = config["cloud_path"]
    Screen.meta_file = config["meta_file"]
    Screen.meta_directory = config["meta_dir"]


def show_message(msg):
    Screen.updateMessage(msg)
    print(msg)

def initWindow():
    root = Tk()
    config = load_configure(error_handling=show_message)
    if config is not None:
        apply_config(config)

    def on_close():
        print("Good bye!")
        save_configure(build_config(), error_handling=show_message)
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.configure(background=dark_back)
    root.title = "Combinator"
    root.geometry('1000x800')
    root.resizable(width=False, height=False)

    initMetaFragment(root)
    initGeneralFragment(root)
    initOptionFragment(root)

    root.mainloop()
