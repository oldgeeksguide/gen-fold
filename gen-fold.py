#!/usr/local/bin/python3

#BUG - -g 4 doesn't do the last line properly (doesn't go all the way to top)
### -l has similar problems

from __future__ import division
from __future__ import print_function
import argparse
import sys

def main():
    args = argparse.ArgumentParser(description='''
Generate an SVG with thin lines for laser cutting to fold wood.
Try this as a decent example:

'python3 gen-fold.py -g 2 -l 21 300 500 5 > foo.svg'

''')
    args.add_argument('width', type=int)
    args.add_argument('height', type=int)
    args.add_argument('num_gaps', type=int,
                       help='Number of gaps in first vertical line')
    # Not using out_file yet
    #args.add_argument('out_file', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
    #                  help='output file (defaults to stdout)')
    args.add_argument('-l', '--lines', dest='lines', metavar='num-vert-lines', type=int,
                       help='Number of vertical lines (by default determines by gap)')
    args.add_argument('-g', '--gap-percentage', dest="gap_percent", metavar='gap%', type=float,
                      default=5,
                      help='Size of gap as a percentage of height')
    args = args.parse_args()

    svg_head = """
    <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">

    <!-- remove 'style="border:sold"' if you don't want the outside border. -->
    <svg style="border:solid"
         xmlns="http://www.w3.org/2000/svg" version="1.1">
    """

    svg_tail = """
    </svg>
    """

    w = args.width
    h = args.height

    # Stroke and fill settings for thin lines (and close path)
    line_settings = '" fill="none" stroke="black" stroke-width="1"/>'

    # Create top and bottom lines (box top and bottom)
    box = '<path d="M10,10 '    # Initial position, upper left corner
    box += 'l'+str(w)+',0 '     # Line across top
    box += 'M10,'+str(h+10)+' '     # Move to lower left corner
    box += 'l'+str(w)+',0'      # Line across bottom
    box += line_settings

    print(svg_head);
    print(box);

    gap_ratio = args.gap_percent/100
    num_gaps =args.num_gaps

    num_slots = num_gaps
    gap = gap_ratio*h
    odd_slot_length = (h-num_gaps*gap)/num_slots
    # num slots on even lines is more, like num gaps,but 2 slots are half length
    even_slot_length = (h-(num_gaps+1)*gap)/num_slots
    if args.lines:
        lines = args.lines
    else:
        lines = int (w/gap)+1

    hgap = w/(lines-1)

    slot_head='<path d="M10,10 '
    print(slot_head);

    def even_slots(h, l, n, g):
        r=""
        for t in range(n):
            r+=" m0 "+str(g)
            r+=" l0 "+str(l)
        r+=" m0 "+str(g)
        return r

    def odd_slots(h, l, n, g):
        r = " l0 "+str(l/2)
        for t in range(n-1):
            r+=" m0 "+str(g)
            r+=" l0 "+str(l)
        r+=" m0 "+str(g)
        r += " l0 "+str(l/2)
        return r

    for i in range(1,1+lines):
        if i % 2 == 1:
            print(odd_slots(h, odd_slot_length, num_slots, gap))
        else:
            print(even_slots(h, even_slot_length, num_slots, gap))
        print("m"+str(hgap)+" "+str(-1*h))

    slot_tail = line_settings
    print(slot_tail);
    print(svg_tail);

if __name__ == '__main__':
    main()

