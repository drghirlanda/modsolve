Features planned for almonds
============================

User interface
---------------

- Separate design from models, making a design class that is available
  to all models, even non-kernel-machine ones

- The design class can be minimal to start with, just a list of dicts,
  each describing an experimental phase. By default, it will have an
  empty dict as first element (phase 0 being interpreted as the
  initial condition).

- Have a base model class specifying a simple user interface such as:

  + model.train( <design> ) 

  + model.V( <stimulus>, <phase> )

- Have a kernel_machine class implementing a generic kernel machine

- Have subclasses of kernel_machine for various models. Each model has
  its own way of calculating generalization factors. Provide a generic
  class for stimuli specified as vectors as well as classes for
  Pearce's 1987 and 1994 models and the replaced elements model.


Models
------

- Sympy can do differential equations. So we can program a full
  solution of the Rescorla-Wagner model and kernel machine models
  including learning curves.

- Explore various representation scheme that generalize the replaced
  elements model.

- Program solution of comparator theory.


Plotting
--------

- Detach plotting window so that one can continue working without
  closing it.

- Add plots to open window
