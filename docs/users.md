# Users

Comma-separated list of tags to apply to the user. Currently supported by the management plugin:

- `management`: User can access the management plugin
- `policymaker`: User can access the management plugin and manage policies and parameters for the vhosts they have access to.
- `monitoring`: User can access the management plugin and see all connections and channels as well as node-related information.
- `administrator`: User can do everything monitoring can do, manage users, vhosts and permissions, close other user's connections, and manage policies and parameters for all vhosts.

Note that you can set any tag here; the links for the above four tags are just for convenience.

Tags does not grant any permissions, it is just gives info about user. Grants managed by permissions
