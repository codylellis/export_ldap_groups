# export_ldap_groups

Export LDAP Groups into DBedit commands. 

# Scope

Check Point Software, R80.x, R81.x, R82.x Multi-Domain and Standalone Management

# Instructions

1. Move to system in it's own folder and run. 
```python3 export_ldap_groups.py```

2. Make sure new account unit with associated accounts is added. 

3. Apply dbedit file. 
```dbedit -f *_ldapgroups_dbedit.txt```




