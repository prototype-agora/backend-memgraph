from gqlalchemy import match


results = list(
    match().node(labels="AppUser", first_name="anna", variable="u").return_().execute()
)
print(len(results))
