# Auctions

![Auctions](https://user-images.githubusercontent.com/83538534/147216894-4cdadb2a-7f4e-4c70-ba9c-c5cbcb89ddc2.gif)

### An eBay-like e-commerce auction site that allows users to post auction listings, place bids on listings, comment and add listings to a `watchlist`.

- **Create Listing:** Users are able to visit a page to create a new listing. They are be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users are optionally able to provide a URL for an image for the listing and/or a category.

- **Active Listings Page:** The default route of the web application lets users view all of the currently active auction listings. For each active listing, this page displays (at minimum) the title, description, current price, and photo (if one exists for the listing).

- **Listing Page:** Clicking on a listing takes the users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.

- **Watchlist:** Users who are signed in are able to visit a `Watchlist page`, which displays all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.

- **Categories:** Users are able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.

- **Django Admin Interface:** Via the Django admin interface, a site administrator to view, add, edit, and delete any listings, comments, and bids made on the site.

