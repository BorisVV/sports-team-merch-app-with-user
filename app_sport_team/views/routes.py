
from datetime import datetime
from flask import \
        render_template, redirect, url_for, abort, request, flash

from app_sport_team import app
from app_sport_team.tables_setUp import \
            db_session, MerchandiseItems, SoldRecords, GamesDates
from app_sport_team import utils

# For example purpose, this is the first pages displayed.
# :flash: In the base.html there is a block inside the body block that exexutes
# the messsages. uses the syntax (var = get_flashed_messages()) and
# will display messages for users to read and correct inputs, etc.
@app.route('/')
def index(): # TODO: remove in future.
    return render_template('index.html')

# User can enter new items, form is displayed.
@app.route('/addItems/', methods=['GET', 'POST'])
def addItems():
    items = MerchandiseItems.query.all()
    if request.method == 'POST':

        if 'cancel' in request.form:
            flash('The option to add items was canceled!')
            return redirect(url_for('index'))

        else:
            # Save button was clicked.
            # str.capitalize()
            new_name = request.form['name'].capitalize()

            if new_name == "":  # validate input.
                flash('Oops! It cannot be blank')
                return redirect(url_for('addItems'))

            for name in items:
                if  name.name == new_name: # if name already in table.
                    flash('Name %r already exist. <br>Try a different one' % new_name)
                    return redirect(url_for('addItems'))

            # The new name will be add if passed the above stataments.
            db_session.add(MerchandiseItems(name=new_name))
            db_session.commit()
            flash('Success! "{}" was added.'.format(new_name) + '<br>Do you want ' \
                    'to add another one? "Cancel to exit"')
            return redirect(url_for('addItems')) # option to add more.

    return render_template('addItems.html', items=items)

@app.route('/displayItems/')
def displayItems():
    items=MerchandiseItems.query.all()
    if not items:
        flash('There are not items in db. Add some first.')
        return redirect(url_for('addItems'))
    return render_template('displayItems.html', items=items)

@app.route('/editItems/', methods=['GET', 'POST'])
def editItems():
    
    items = MerchandiseItems.query.all()

    if request.method == 'POST':
        name = MerchandiseItems.query.get(int(request.form['name_selected']))
        new_name = request.form['new_name']
        #Let's get the items in sold records.
        items_in_sold_rec = SoldRecords.query.filter_by(item_id=name.id).all()
        print('name ', name)

        if 'cancel' in request.form:
            flash('Transaction canceled.')

        elif 'delete' in request.form:
            old_name = name.name # Store old name.
            for item in items_in_sold_rec:
                db_session.delete(item)
                db_session.commit()
            db_session.delete(name)
            db_session.commit()
            flash('{} was deleted as well those in the sold records. <br> \
                    Do you want to delete/update more. <br> \
                    "Cancel" to quit.'.format(old_name))
            return render_template('editItems.html', items=MerchandiseItems.query.all())

        else:
            if new_name == "":
                flash('Text box cannot be blank, name required! <br> \
                        Enter new  name for the selected name! --> ' + name.name)
                return render_template('editItems.html', items=items, name_id=name.id)
            if new_name == name.name:
                flash('{} name is already selected, nothing was updated!'.format(name.name))
                return render_template('editItems.html', items=items, name_id=name.id)

            try:
                old_name = name.name # Stored to display old name.
                name.name = new_name.capitalize() # Change the name.
                db_session.commit()
                # Display message.
                flash('"{}" was updated succesfully! with --> "{}."' \
                        .format(old_name, name.name))
                flash('Do you want to delete/update another? "Cancel" to quit')
                # Render the template again with the updated item selected.
                return render_template('editItems.html', items=MerchandiseItems.query.all(), name_id=name.id)
            except:
                db_session.rollback() # If not Exception will raise.
                flash('%r is already in file, try a different name' % new_name)
                # Re-render the template with the users inputs.
                return render_template('editItems.html', items=items, item_id=name.id, new_name=new_name)

    return render_template('editItems.html', items=items)

@app.route('/addDates/', methods=['GET', 'POST'])
def addDates():
    # Collect the date, city and state for the game.
    if request.method == 'POST':
        date_game = request.form['date_game']
        city = request.form['city']
        state = request.form['state']

        if 'cancel' in request.form:
            flash('The add dates option was canceled!')
            return redirect(url_for('index'))

        else:
            # This is to make sure that boxes are not empty.
            if date_game == '' or city == '' or state == '':
                flash('No blank text boxes allowed!')
                return render_template('addDates.html', date_game=date_game, \
                city=city, state=state)

            # Need to validate the input and make sure that date in not
            # already in db.
            try:
                dt = utils.format_date(date_game)
                db_session.add(GamesDates(_date=dt, city=city, state=state.upper()))
                db_session.commit()
                flash('Success! <br> \
                Date: {}, City: {}, State: {} <br> \
                was added to Games\' Schedules <br>  \
                Would you like to add more? \'Cancel\' to exit.' \
                .format(date_game, city, state)
                )
                return redirect(url_for('addDates'))
            except:
                db_session.rollback()
                flash('Date {} is already in file it can\'t be used twice!'.format(date_game))

                return render_template('addDates.html',\
                    date_game=date_game, city=city, state=state)

    return render_template('addDates.html')

@app.route('/displayGameSched/')
def displayGameSched():
    _dates=GamesDates.query.all()
    if not _dates:
        flash('There are not dates in db. Add some first.')
        return redirect(url_for('addDates'))
    return render_template('displayGameSched.html', _dates=_dates)

@app.route('/editDates/<int:id>/', methods=['GET', 'POST'])
def editDates(id):
    sched = GamesDates.query.get(id)
    dates_in_soldRecords = SoldRecords.query.filter_by(date_id=id).all()

     # category = Category.query.filter_by(slug=slug).first()
     # snippets = category.snippets.order_by(Snippet.title).all()

    # Date is in the form Y-m-d @ m:s:.etc which is bad for
    # reding, the strftime solves that problem.
    dt = datetime.strftime(sched._date, '%Y-%m-%d')

    # This is to display the deleted information.
    dt_str = tuple((dt, str(sched.city), str(sched.state)))

    form = dict(_date=sched._date, city=sched.city, state=sched.state)
    if request.method == 'POST':

        # Format date to convert it to sqlalchey DateTime
        form['_date'] = utils.format_date(request.form['date'])
        form['city'] = request.form['city']
        form['state'] = request.form['state']
        # If the boxes are left blank.
        if form['_date'] == "":
            form['_date'] = sched._date
        if form['city'] == "":
            form['city'] = sched.city
        if form['state'] == "":
            form['state'] = sched.state

        if 'cancel' in request.form:
            return redirect(url_for('index'))

        # Assuming that nothing goes wrong.
        elif 'delete' in request.form:
            db_session.delete(sched)
            for record in dates_in_soldRecords:
                db_session.delete(record)
            db_session.commit()
            flash('Deleted ' + str(dt_str))
            return redirect(url_for('displayGameSched'))

        else:
            try:
                if form['_date'] == sched._date and \
                        form['city'] == sched.city and \
                        form['state'] == sched.state:
                    flash('Nothing was updated!!')
                    return render_template('editDates.html', form=form, sched=sched)
                else:
                    # Update the data.
                    sched._date = form['_date']
                    sched.city = form['city']
                    sched.state = form['state']
                    db_session.commit()
                    flash('Date was updaed succesfully!')
                    return render_template('editDates.html', form=form, sched=sched)
            except:
                flash('Something went wrong, check the inputs.')
                return redirect(url_for('editDates'))
    return render_template('editDates.html', form=form, sched=sched)

@app.route('/addSoldRecord/', methods=['GET', 'POST'])
def addSoldRecord():
    items = MerchandiseItems.query.all()
    _dates = GamesDates.query.all()
    soldRec = SoldRecords.query.all()

    # We need to verify that there are records in db. first.
    if not items:
        flash('Warning!!! <br> There not items in db, you first need to add items.<br>' \
                'Then you can add Sold Records.')
        return redirect(url_for('addItems'))
    if not _dates:
        flash('Warning!!! <br> There not dates in db, you first need to add dates.<br>' \
                'Then you can add Sold Records.')
        return redirect(url_for('addDates'))


    # TODO:  Create a form dict for render_template.

    if request.method == 'POST':

        if 'cancel' in request.form:
            flash('Transaction canceled!')
            return redirect(url_for('displaySoldRecords'))

        else: # Save was clicked.
            # In the html there is a select and options. The values/id are
            # collected from the select for both item and date.

            # This two lines below are for example only/ both get the full row
            # name_row = MerchandiseItems.query.get(request.form['selected_item'])
            # _date_row = GamesDates.query.get(request.form['selected_date'])

            date_id = int(request.form['selected_date'])
            item_id = int(request.form['selected_item'])
            # For qty the box is a numeric type so theres no need to convert it.
            qty = request.form['quantity']
            # For price the box is a text type and needs to be converted to float.
            price = request.form['price']

            for row in soldRec:
                if date_id == row.date_id and item_id == row.item_id:
                    _date = str(row.schedules._date).replace('00:00:00', ' ')
                    flash('Warning!!! <br> Transaction canceled!')
                    flash('Name= {} and Date= {} is already in file. <br> \
                           Go to link above "sold records" to edit the record.' \
                    .format(row.items.name, _date))

                    return render_template('addSoldRecord.html',\
                                    items=items, _dates=_dates, item_id=item_id, \
                                    date_id=date_id, qty=qty, price=price)

            try:
                price = float(price)
                # for small example we need to keep numbers small.
                if price < 0 or price > 150:
                    flash('Make sure the price is between 0.00 and 150.00.\
                    <br>You entered %r' % price)
                    return render_template('addSoldRecord.html',\
                    items=items, _dates=_dates, item_id=item_id, \
                    date_id=date_id, qty=qty, price='')
            except:
                # The input was a string not a numeric value.
                flash('Check box price and make sure is a numeric value. <br>\
                        You entered {}'.format(price))
                return render_template('addSoldRecord.html',\
                                    items=items, _dates=_dates, item_id=item_id, \
                                    date_id=date_id, qty=qty, price=price)

            # If not nothing fails above.
            db_session.add(SoldRecords(item_id=item_id, date_id=date_id, qty=qty, price=price))
            db_session.commit()
            flash('Record added and saved succesfully! <br> Add more?')
            return render_template('addSoldRecord.html', date_id=date_id, item_id=item_id, price=price, qty=qty, _dates=_dates, items=items)

    return render_template('addSoldRecord.html', items=items, _dates=_dates)

@app.route('/displaySoldRecords/')
def displaySoldRecords():
    itemsSold = SoldRecords.query.order_by(SoldRecords.item_id).all()
    if not itemsSold:
        flash('Warning!!! <br> There are not sold records in db. Add some first!')
    return render_template('displaySoldRecords.html', itemsSold=itemsSold)

@app.route('/editSoldRecords/<int:id>/', methods=['GET', 'POST'])
def editSoldRecords(id):
    # id is from the displaySoldRecords.html
    modifySold = SoldRecords.query.get(id)
    _dates = GamesDates.query.all()
    names = MerchandiseItems.query.all()

    if request.method == 'POST':
        date_id = int(request.form['date_selected'])
        item_id = int(request.form['name_selected'])
        qty = int(request.form['quantity'])
        price = request.form['price']

        if 'cancel' in request.form:
            flash('Transaction canceled!')
            return redirect(url_for('index'))

        elif 'delete' in request.form:
            db_session.delete(modifySold)
            db_session.commit()
            flash('Record deleted!')
            return redirect(url_for('displaySoldRecords'))

        else:
            # print('date', date_id, 'item', item_id, 'qty', qty, 'price', price)
            # print('modidfadsf', modifySold, modifySold.date_id, modifySold.item_id)
            # The table takes a float for price, try/except is very handy here.
            try:
                price = float(price)

                if date_id == modifySold.date_id and \
                        item_id == modifySold.item_id and \
                        qty == modifySold.qty and \
                        price == modifySold.price:
                    flash('Ther were no changes made!')
                    return redirect(url_for('displaySoldRecords'))

                elif date_id == modifySold.date_id and \
                        item_id == modifySold.item_id and \
                        qty != modifySold.qty or \
                        price != modifySold.price:
                    modifySold.qty = qty
                    modifySold.price = price
                    db_session.commit()
                    flash('Either quantity/price or both were succesfully updated!')
                    return redirect(url_for('displaySoldRecords'))
                else:
                    no_matched = True
                    for row in SoldRecords.query.all():
                        if date_id == row.date_id and item_id == row.item_id:
                            no_matched = False
                            flash('{} and {} already in sold rec "{}" and "{}"'.format(date_id, item_id, modifySold, row))
                            return render_template('editSoldRecords.html', _dates=_dates, names=names, modifySold=modifySold)
                    if no_matched:
                        modifySold.date_id = date_id
                        modifySold.item_id = item_id
                        modifySold.qty = qty
                        modifySold.price = price
                        db_session.commit()
                        flash('Data was updated succesfully!!')
                        return redirect(url_for('displaySoldRecords'))
            except Exception as e:
                db_session.rollback()
                flash('Error  <br>'+ str(e))
                return redirect(url_for('displaySoldRecords'))

    return render_template('editSoldRecords.html', \
                            modifySold=modifySold, _dates=_dates, \
                            names=names)
