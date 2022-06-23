from PIL import Image, ImageDraw, ImageFont


def percentage_display(percentages):
    
    nb_bars = len(percentages)

    bar_height = 150
    height_between_bars = 80
    bar_width = 900

    width_margin = 10
    height_margin = 10
    image_width = bar_width + 2*width_margin
    image_height = nb_bars*(bar_height+height_between_bars) + 2*height_margin

    # (0,0) is upper-left corner

    image  = Image.new( mode = "RGBA", size = (image_width, image_height), color = (0,0,0,0) )
    draw = ImageDraw.Draw(image)

    radius = 20
    bar_outline_width = 5
    fill_outline_width = 1

    # sample text and font

    font_size = 50
    lato_font = ImageFont.truetype("~/.share/fonts/Lato-Regular.ttf", font_size, encoding="unic")
    text_color = "white"
    text_outline_width = 2
    text_outline_color = "black"

    colors_list=["blue", "red", "green"]

    for i in range(nb_bars):

        # create the bar to be filled 
        top_left_point = (width_margin, height_margin+i*bar_height+i*height_between_bars)
        bottom_right_point = (width_margin+bar_width, height_margin+(i+1)*bar_height+i*height_between_bars)

        xy_bar = [top_left_point, bottom_right_point]

        draw.rounded_rectangle(xy_bar, radius=radius, fill=(255, 255, 255, 125), outline="black", width=bar_outline_width)

        # fill the bar
        top_left_point_fill = (width_margin+bar_outline_width, height_margin+i*bar_height+i*height_between_bars+bar_outline_width)
        bottom_right_point_fill = ((width_margin+bar_width)*percentages[i], height_margin+(i+1)*bar_height+i*height_between_bars-bar_outline_width)
        xy_fill = [top_left_point_fill, bottom_right_point_fill]

        draw.rounded_rectangle(xy_fill, radius=radius-bar_outline_width, fill=colors_list[i], outline="white", width=fill_outline_width)

        # add the percentage as text in the bar

        bar_to_text_anchor_width = bar_width//10
        bar_to_text_anchor_height = bar_height//2
        text_anchor_coords = (width_margin+bar_outline_width+bar_to_text_anchor_width, height_margin+i*bar_height+i*height_between_bars+bar_to_text_anchor_height)

        in_bar_text = str(percentages[i]*100)+" %"
        draw.text(text_anchor_coords, text=in_bar_text, fill=text_color, font=lato_font, anchor='lm', spacing=4, align='left', direction=None, features=None, language=None, stroke_width=text_outline_width, stroke_fill=text_outline_color, embedded_color=False)
    


    image.save("test_image.png")
    image.show()


percentages = [0.254,0.890] # from 0 to 1
percentage_display(percentages)







