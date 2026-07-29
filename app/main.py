from camera.camera import Camera


def main():
    camera = Camera()

    try:
        camera.open()
        camera.show()

    finally:
        camera.release()


if __name__ == "__main__":
    main()