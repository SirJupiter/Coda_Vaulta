#!/usr/bin/python3
""" console.py

Main purpose of the console is to test the models created and
be sure that they work as intended, before redirecting CRUD to
database on server and implementing MySQL database definition schema
 """

import cmd
import models
from models.user import User
from models.snippet import Snippet
import shlex  # for splitting the line along spaces except in double quotes

classes = {"User": User, "Snippet": Snippet}


class CODAVAULTAConsole(cmd.Cmd):
    """ CODAVAULTA console """
    prompt = 'CodaVaulta Console $$ '

    def preloop(self):
        """Introductory text before the prompt"""
        print("Welcome to the CodaVaulta Console!")
        print("You can create, show, destroy, and manage users and snippets.")
        print('\n')
        print(
            "This console is created to test the models and be sure they "
            "work properly before being integrated with the "
            "API and frontend"
        )
        print("Type 'help' or '?' to list commands.\n")

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return False

        if args[0] in classes:
            new_instance = None
            if args[0] == 'User':
                if len(args) < 4:
                    print("** username, email or password is missing **")
                    return False

                args[1] = args[1].replace('-', ' ')
                username, email, password = args[1], args[2], args[3]
                if len(password) < 8:
                    print("** password must be at least 8 characters long **")
                    return False
                new_instance = User(username, email, password)

            elif args[0] == 'Snippet':
                if len(args) < 5:
                    print("** title, code, or user id is missing **")
                    return False

                title, code, desc, user_id = args[1], args[2], args[3], args[4]
                code, desc = code.replace('-', ' '), desc.replace('-', ' ')

                user = models.storage.get_user_by_user_id(user_id)
                if not user:
                    print("** user doesn't exist **")
                    return False
                new_instance = Snippet(title, code, desc, user_id)
            else:
                print("** class doesn't exist **")
                return False

            models.storage.new(new_instance)
            models.storage.save()
            print(new_instance.to_dict())
        else:
            print("** class doesn't exist **")
            return False

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                obj = None
                if args[0] == 'User':
                    obj = models.storage.get_user_by_user_id(args[1])
                elif args[0] == 'Snippet':
                    obj = models.storage.get_snippet_by_snippet_id(args[1])
                if not obj:
                    print("** no instance found **")
                else:
                    print(obj.to_dict())
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                obj = None
                if args[0] == 'User':
                    obj = models.storage.get_user_by_user_id(args[1])
                elif args[0] == 'Snippet':
                    obj = models.storage.get_snippet_by_snippet_id(args[1])
                if not obj:
                    print("** no instance found **")
                else:
                    models.storage.delete(obj)
                    models.storage.save()
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_update_snippet(self, arg):
        """Updates a snippet object"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False

        if args[0] == 'Snippet':
            if len(args) > 1:
                if len(args) < 5:
                    print("** snippet_id, title, code, "
                          "or description is missing **")
                    return False

                snip_id, title, code, desc = args[1], args[2], args[3], args[4]
                code, desc = code.replace('-', ' '), desc.replace('-', ' ')

                snippet = models.storage.update_snippet(
                    snip_id, title, code, desc)
                if not snippet:
                    print("** no instance found **")
                else:
                    print(snippet.to_dict())
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    # def do_all(self, arg):
    #     """Prints string representations of instances"""
    #     args = shlex.split(arg)
    #     obj_list = []
    #     if len(args) == 0:
    #         obj_dict = models.storage.all()
    #     elif args[0] in classes:
    #         obj_dict = models.storage.all(classes[args[0]])
    #     else:
    #         print("** class doesn't exist **")
    #         return False
    #     for key in obj_dict:
    #         obj_list.append(str(obj_dict[key]))
    #     print("[", end="")
    #     print(", ".join(obj_list), end="")
    #     print("]")


if __name__ == '__main__':
    CODAVAULTAConsole().cmdloop()
