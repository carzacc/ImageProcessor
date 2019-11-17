from imageprocessor import ImageProcessor


def process_dir(args):
    image_processor = ImageProcessor(args.dir, args.save_dir)
    image_processor.process_dir()


def copy(args):
    image_processor = ImageProcessor(args.dir, args.save_dir, process=False)
    image_processor.process_dir()
