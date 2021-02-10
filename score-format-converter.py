import music21
import os,sys,time
from gooey import Gooey,GooeyParser


# param
FORMAT_LIST = ['midi','xml','krn','abc','humdrum','mei'] # more than that
OUTPUT_FOLDNAME = "output"


@Gooey(program_name="Easy Musical Score Converter",
       default_size=(480,360),
       progress_regex=r"^progress: (\d+)%$")
def main():
    
    parser = GooeyParser(description="A small tool for parsing & converting multi musical score formats."+"\r\n"+"The converted file will be in <output> directory.")
    parser.add_argument('Directory',widget="DirChooser",help="Select a directory that consists of original scores.")
    parser.add_argument('Format',widget="FilterableDropdown",help="Choose the output format that listed below.",choices=FORMAT_LIST)
    args = parser.parse_args()

    fmt = args.Format
    input_dir = args.Directory
    success = 0 
    fail = 0
    score_list = [f for f in os.listdir(input_dir) if not f.startswith('.')]
    
    start = time.time()
    
    output_dir = input_dir + '/' + OUTPUT_FOLDNAME + '-' + fmt
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for score in score_list:
        try:
            converter(os.path.join(input_dir,score),fmt,output_dir)
            success += 1
        except Exception as e:
            fail += 1
        continue

    print("Conversion is completed! Total: {} sec.".format(time.time()-start))
    print("Success:{} ; Fail:{}".format(success,fail))


def converter(score,fmt,output_dir):
    s = music21.converter.parse(score)
    s_name,_ = os.path.splitext(os.path.basename(score))
    s.write(fmt,"{}/{}.{}".format(output_dir,s_name,fmt))

if __name__ == '__main__':
    main()