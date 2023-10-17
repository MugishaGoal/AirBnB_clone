#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    """
    Parse a given string and split it into a list of elements
    based on curly braces and brackets.
    """
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)

    if curly_braces is None and brackets is None:
        return [i.strip(",") for i in arg.split()]

    result_list = []

    if curly_braces is not None:
        lexer = arg[:curly_braces.span()[0]].split()
        result_list.extend([i.strip(",") for i in lexer])
        result_list.append(curly_braces.group())

    if brackets is not None:
        lexer = arg[:brackets.span()[0]].split()
        result_list.extend([i.strip(",") for i in lexer])
        result_list.append(brackets.group())

    return result_list


class HBNBCommand(cmd.Cmd):
    """
    Defines the HolbertonBnB command interpreter's purpose.

    Attributes:
        prompt (str): The command prompt.
    """
    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Take no action when an empty line is received."""
        pass

    def default(self, arg):
        """Default behavior for cmd module incase the input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """A command used to exit the program."""
        return True

    def do_EOF(self, arg):
        """An EOF signal used to terminate the program."""
        print("")
        return True

    def do_create(self, arg):
        """
        Usage: create <class>
        Create a new class instance and print its id.
        """
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """
        Usage: show <class> <id> or <class>.show(<id>)
        Displays the string representation of a class instance of a given id.
        """
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """
        Usage: destroy <class> <id> or <class>.destroy(<id>)
        Deletes a class instance of a given id.
        """
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """
        Usage: all or all <class> or <class>.all()
        Displays string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        """
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """
        Usage: count <class> or <class>.count()
        Retrieves the number of instances of a given class.
        """
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """
        Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Updates a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        """
        args = parse(arg)
        objdict = storage.all()

        if len(args) < 2:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        if len(args) < 3:
            print("** instance id missing **")
            return

        obj_key = "{}.{}".format(class_name, args[1])
        if obj_key not in objdict:
            print("** no instance found **")
            return

        obj = objdict[obj_key]

        if len(args) < 4:
            print("** attribute name missing **")
            return

        attr_name = args[2]
        if len(args) == 4:
            attr_value = args[3]
            setattr(obj, attr_name, attr_value)
        elif len(args) == 3 and isinstance(eval(args[2]), dict):
            attr_dict = eval(args[2])
            for key, value in attr_dict.items():
                setattr(obj, key, value)

        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
