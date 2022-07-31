# mtg_pricer
The goal of this project is to analyze a decklist of cards owned and cards to buy and be able to find prices for the cards to purchase. This should simplifiy the deck construciton process.

# Files needed:
Download the Scryfall bulk-data from the website. Based on the 'All Cards' dataset.

https://scryfall.com/docs/api/bulk-data

Link Used:
    https://c2.scryfall.com/file/scryfall-bulk/all-cards/all-cards-20220320211331.json

# 06/14/2022 UPDATE
Added the ability to download CLB leaders and backgrounds with images tagged to the JSON.

Images are .png and stored in card_data/card_images/

Two files created with appended 'local' tags for images as they are saved with name_collectornumber.png
1. backgrounds.json
2. cobcreatures.json

New file to create background pairs... Currently working on implementing, then having the cards displayed.

Test Upload