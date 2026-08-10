from registration.registration import Registration
from admin.admin import Admin
from recognition.recognition import Recognition


def main():
    """Main menu."""

    while True:

        print("\n========== FACE RECOGNITION ATTENDANCE ==========")
        print("1. Register Student")
        print("2. View Students")
        print("3. Delete Student")
        print("4. Recognize Student")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":

            registration = Registration()
            registration.register_student()

        elif choice == "2":

            admin = Admin()
            admin.view_students()
            admin.close()

        elif choice == "3":

            admin = Admin()
            admin.delete_student()
            admin.close()

        elif choice == "4":

            recognition = Recognition()
            recognition.start()

        elif choice == "5":

            print("\nGoodbye!")
            break

        else:

            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()