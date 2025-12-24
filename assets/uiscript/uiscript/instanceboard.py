import uiScriptLocale

ROOT = "d:/ymir work/ui/public/"

window = {
	"name" : "InstanceBoard",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH/2 - 200,
	"y" : SCREEN_HEIGHT/2 - 250,

	"width" : 400,
	"height" : 500,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 400,
			"height" : 500,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : 384,
					"color" : "yellow",

					"children" :
					(
						{
							"name":"TitleName",
							"type":"text",
							"x":192,
							"y":3,
							"text":"Private Instance Manager",
							"horizontal_align":"center",
							"text_horizontal_align":"center"
						},
					),
				},

				## Current Map Info
				{
					"name" : "map_info_bg",
					"type" : "image",
					"x" : 15,
					"y" : 35,
					"image" : ROOT + "Parameter_Slot_03.sub",

					"children" :
					(
						{
							"name" : "current_map_label",
							"type" : "text",
							"x" : 10,
							"y" : 8,
							"text" : "Current Map:",
							"color" : 0xFFFFE3AD,
						},
						{
							"name" : "current_map_name",
							"type" : "text",
							"x" : 100,
							"y" : 8,
							"text" : "",
							"color" : 0xFFFFFFFF,
						},
					),
				},

				## Map List Title
				{
					"name" : "map_list_title",
					"type" : "text",
					"x" : 15,
					"y" : 70,
					"text" : "Available Maps:",
					"color" : 0xFFFFE3AD,
				},

				## Scrollable Map List
				{
					"name" : "map_list_bg",
					"type" : "box",
					"x" : 15,
					"y" : 90,
					"width" : 370,
					"height" : 330,
					"color" : 0x77000000,
				},

				## Instance Status Warning
				{
					"name" : "instance_status",
					"type" : "text",
					"x" : 200,
					"y" : 425,
					"text" : "",
					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"color" : 0xFFFF4444,
				},

				## Info Text
				{
					"name" : "info_text",
					"type" : "text",
					"x" : 200,
					"y" : 445,
					"text" : "Click on a map to create your private instance",
					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"color" : 0xFF999999,
				},

				## Exit Instance Button
				{
					"name" : "exit_button",
					"type" : "button",

					"x" : 130,
					"y" : 465,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					"text" : "Exit Instance",

					"default_image" : ROOT + "large_button_01.sub",
					"over_image" : ROOT + "large_button_02.sub",
					"down_image" : ROOT + "large_button_03.sub",
				},

				## Close Button
				{
					"name" : "close_button",
					"type" : "button",

					"x" : 270,
					"y" : 465,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					"text" : "Close",

					"default_image" : ROOT + "middle_button_01.sub",
					"over_image" : ROOT + "middle_button_02.sub",
					"down_image" : ROOT + "middle_button_03.sub",
				},
			),
		},
	),
}
