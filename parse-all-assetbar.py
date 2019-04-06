import assetbar_parser
import glob

for filename in glob.glob("assetbar/*.html"):
    print(filename)
    assetbar_parser.parse_file(filename)
