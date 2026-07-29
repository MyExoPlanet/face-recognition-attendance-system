from camera.camera import Camera


def main():
    camera = Camera()

    try:
        camera.open()

        frame = camera.read()

        print(frame.shape)

    finally:
        camera.release()


if __name__ == "__main__":
    main()