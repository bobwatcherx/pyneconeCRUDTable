import pynecone as pc
# NOW IMPORT MODEL
from .models.food import Foods

class State(pc.State):
    name:str
    price:int
    stock:int
    id_edit:int

    # NOW I USE MODAL IF YOU CLICK BUTTON EDIT
    # DEFAULT IS FALSE 
    # IF YOU CLICK EDIT BUTTON THEN MODAL IS OPEN

    show_modal:bool = False



    def open_modal(self):
        self.show_modal = not (self.show_modal)


    # FOR ADD NEW DATA
    def addNew(self):
        if self.name and self.price and self.stock:
            try:
                with pc.session() as s:
                    s.add(
                        Foods(
                        food_name=self.name,
                        price=self.price,
                        stock=self.stock
                            )

                        )
                    s.commit()
            except Exception as e:
                print(e)
        else:
            print("please fill all field before adding")


    # EXTRACT ALL DATA FROM TABLE SQLITE
    @pc.var
    def get_data(self)-> list[Foods]:
        with pc.session() as s:
            self.users = s.query(Foods).all()
            return self.users


    # FOR DELETE DATA FROM TABLE
    def delete_data(self,id_delete):
        with pc.session() as s:
            s.query(Foods).filter_by(id=id_delete).delete()
            s.commit()


    # FOR EDIT DATA FROM TABLE

    def edit_data(self,user):
        print(user)
        # AND OPEN MODAL 
        self.show_modal = True
        # NOW I SET TEXTFIELD NAME PRICE AND STOCK FROM YOU
        # SELECTED DATA
        self.name = user['food_name']
        self.price = int(user['price'])
        self.stock = int(user['stock'])
        self.id_edit = user['id']


    # FOR SAVE 
    def save_data(self):
        with pc.session() as s:
            # NOW I CREATE QUERY FOR FIND YOU ID FROM TABLE
            food = s.query(Foods).filter_by(id=self.id_edit).first()
            print(food)
            if food is not None:
                food.food_name  = self.name
                food.price  = self.price
                food.stock  = self.stock
                s.commit()

                # AND CLOSE MODAL
                self.show_modal = False
            else:
                # IF NOT FOUND 
                print("found is not found ",id_edit)


# NOW I CREATE LOOP pc.td  IN TABLE TBODY
def showalldata(user:Foods):
    print(user)
    return pc.tr(
        pc.td(user.food_name),
        pc.td(user.price),
        pc.td(user.stock),
        # AND I CREATE EDIT AND DELETE BUTTON FROM BODY TABLE
        pc.td(
            pc.button("Edit",
                bg="blue",
                color="white",
                on_click=lambda:State.edit_data(user)
                ),
             pc.button("Delete",
                bg="red",
                color="white",
                on_click=lambda:State.delete_data(user.id)
                ),
            )


        )


def index():
    return pc.vstack(
        pc.heading("crud pynecone",size="md"),
        pc.input(
            focus_border_color="purple",
            placeholder="Food Name",
            on_change=State.set_name
            ),
        pc.input(
            focus_border_color="purple",
            placeholder="Price",
            on_change=State.set_price
            ),
        pc.input(
            focus_border_color="purple",
            placeholder="Stock",
            on_change=State.set_stock
            ),
        pc.button("add new",
            bg="blue",
            color="white",
            size="lg",
            on_click=State.addNew
            ),

        # NOW I CREATE TABLE CONTAINER
        pc.table_container(
            pc.table(
                pc.thead(
                    pc.tr(
                        pc.th("name"),
                        pc.th("price"),
                        pc.th("stock"),
                        )
                    ),
                # NOW LOOP DATA FROM TABLE TO BODY TABLE
                pc.tbody(pc.foreach(State.get_data,showalldata))

                )
            ),
        # MODAL HERE
        pc.modal(
            pc.modal_overlay(
                pc.modal_content(
                pc.modal_header("Edit data"),
                pc.modal_body(
                    pc.vstack(
                    pc.input(
                        placeholder="EDIT NAME",
                        on_change=State.set_name,
                        value=State.name
                        ),
                     pc.input(
                        placeholder="EDIT NAME",
                        on_change=State.set_price,
                        ),
                      pc.input(
                        placeholder="EDIT NAME",
                        on_change=State.set_stock,
                        ),

                        )
                    ),
                # AND I CREATE SAVE BUTTON AND CLOSE BUTTON
                pc.button("Save",
                    bg="blue",
                    color="white",
                    on_click=State.save_data
                    ),
                pc.button("Close",
                    # THIS WIL CLOSE MODAL
                    on_click=State.open_modal
                    ),
                    )
                ),
            is_open=State.show_modal

            )

        )




app = pc.App(state=State)
app.add_page(index)
app.compile()
