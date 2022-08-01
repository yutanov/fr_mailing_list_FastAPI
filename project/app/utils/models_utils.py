def update_model(db_model, model_update):
    for var, value in vars(model_update).items():
        if vars(db_model).get(var) is None:
            continue
        setattr(db_model, var, value) if value else None

    return db_model


def enum_elements_to_string(enum):
    return "\n".join([f'{x.name} - {int(x)}' for x in enum])
