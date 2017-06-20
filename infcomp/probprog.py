#
# Oxford Inference Compilation
# https://arxiv.org/abs/1610.09900
#
# Tuan-Anh Le, Atilim Gunes Baydin
# University of Oxford
# May 2016 -- May 2017
#

class Sample(object):
    def __init__(self):
        self.address = None
        self.address_suffixed = None
        self.instance = None
        self.value = None
        self.value_dim = None
        self.distribution = None
        self.lstm_input = None
        self.lstm_output = None
    def __repr__(self):
        return 'Sample({0}, {1}, {2}, {3}, {4})'.format(self.address, self.address_suffixed, self.instance, self.value.size(), str(self.distribution))
    __str__ = __repr__
    def cuda(self, device_id=None):
        if not self.value is None:
            self.value = self.value.cuda(device_id)
        self.distribution.cuda(device_id)
    def cpu(self):
        if not self.value is None:
            self.value = self.value.cpu()
        self.distribution.cpu()

class Trace(object):
    def __init__(self):
        self.observes = None
        self.observes_embedding = None
        self.samples = []
        self.length = None
    def __repr__(self):
        return 'Trace(length:{0}, samples:[{1}], observes.dim():{2})'.format(self.length, ', '.join([str(sample) for sample in self.samples]), self.observes.dim())
    __str__ = __repr__
    def addresses(self):
        return '|'.join([sample.address for sample in self.samples])
    def addresses_suffixed(self):
        return '|'.join([sample.address_suffixed for sample in self.samples])
    def set_observes(self, o):
        self.observes = o
    def add_sample(self, s):
        self.samples.append(s)
        self.length = len(self.samples)
    def cuda(self, device_id=None):
        if not self.observes is None:
            self.observes = self.observes.cuda(device_id)
        for i in range(len(self.samples)):
            self.samples[i].cuda(device_id)
    def cpu(self):
        if not self.observes is None:
            self.observes = self.observes.cpu()
        for i in range(len(self.samples)):
            self.samples[i].cpu()

class UniformDiscrete(object):
    def __init__(self, prior_min, prior_size):
        self.prior_min = prior_min
        self.prior_size = prior_size
        self.proposal_probabilities = None

        self.name = 'UniformDiscrete'
        self.address_suffix = '_UniformDiscrete(prior_min:{0}, prior_size:{1})'.format(self.prior_min, self.prior_size)
    def __repr__(self):
        return 'UniformDiscrete(prior_min:{0}, prior_size:{1}, proposal_probabilities:{2})'.format(self.prior_min, self.prior_size, self.proposal_probabilities)
    __str__ = __repr__
    def set_proposalparams(self, proposal_probabilities):
        self.proposal_probabilities = proposal_probabilities
    def cuda(self, device_id=None):
        if not self.proposal_probabilities is None:
            self.proposal_probabilities = self.proposal_probabilities.cuda(device_id)
    def cpu(self):
        if not self.proposal_probabilities is None:
            self.proposal_probabilities = self.proposal_probabilities.cpu()

class UniformContinuous(object):
    def __init__(self, prior_min, prior_max):
        self.prior_min = prior_min
        self.prior_max = prior_max
        self.proposal_mode = None
        self.proposal_certainty = None

        self.name = 'UniformContinuous'
        self.address_suffix = '_UniformContinuous'
    def __repr__(self):
        return 'UniformContinuous(prior_min:{0}, prior_max:{1}, proposal_mode:{2}, proposal_certainty:{3})'.format(self.prior_min, self.prior_max, self.proposal_mode, self.proposal_certainty)
    __str__ = __repr__
    def set_proposalparams(self, tensor_of_proposal_mode_certainty):
        self.proposal_mode = tensor_of_proposal_mode_certainty[0]
        self.proposal_certainty = tensor_of_proposal_mode_certainty[1]
    def cuda(self, device_id=None):
        return
    def cpu(self):
        return

class Normal(object):
    def __init__(self, prior_mean, prior_std):
        self.prior_mean = prior_mean
        self.prior_std = prior_std
        self.proposal_mean = None
        self.proposal_std = None

        self.name = 'Normal'
        self.address_suffix = '_Normal'
    def __repr__(self):
        return 'Normal(prior_mean:{0}, prior_std:{1}, proposal_mean:{2}, proposal_std:{3})'.format(self.prior_mean, self.prior_std, self.proposal_mean, self.proposal_std)
    __str__ = __repr__
    def set_proposalparams(self, tensor_of_proposal_mean_std):
        self.proposal_mean = tensor_of_proposal_mean_std[0]
        self.proposal_std = tensor_of_proposal_mean_std[1]
    def cuda(self, device_id=None):
        return
    def cpu(self):
        return

class Flip(object):
    def __init__(self):
        self.proposal_probability = None

        self.name = 'Flip'
        self.address_suffix = '_Flip'
    def __repr__(self):
        return 'Flip(proposal_probability: {0})'.format(self.proposal_probability)
    __str__ = __repr__
    def set_proposalparams(self, tensor_of_proposal_probability):
        self.proposal_probability = tensor_of_proposal_probability[0]
    def cuda(self, device_id=None):
        return
    def cpu(self):
        return

class Discrete(object):
    def __init__(self, prior_size):
        self.prior_size = prior_size
        self.proposal_probabilities = None

        self.name = 'Discrete'
        self.address_suffix = '_Discrete(prior_size:{0})'.format(self.prior_size)
    def __repr__(self):
        return 'Discrete(prior_size:{0}, proposal_probabilities:{1})'.format(self.prior_size, self.proposal_probabilities)
    __str__ = __repr__
    def set_proposalparams(self, proposal_probabilities):
        self.proposal_probabilities = proposal_probabilities
    def cuda(self, device_id=None):
        if not self.proposal_probabilities is None:
            self.proposal_probabilities = self.proposal_probabilities.cuda(device_id)
    def cpu(self):
        if not self.proposal_probabilities is None:
            self.proposal_probabilities = self.proposal_probabilities.cpu()

class Categorical(object):
    def __init__(self, prior_size):
        self.prior_size = prior_size
        self.proposal_probabilities = None

        self.name = 'Categorical'
        self.address_suffix = '_Categorical(prior_size:{0})'.format(self.prior_size)
    def __repr__(self):
        return 'Categorical(prior_size:{0}, proposal_probabilities:{1})'.format(self.prior_size, self.proposal_probabilities)
    __str__ = __repr__
    def set_proposalparams(self, proposal_probabilities):
        self.proposal_probabilities = proposal_probabilities
    def cuda(self, device_id=None):
        if not self.proposal_probabilities is None:
            self.proposal_probabilities = self.proposal_probabilities.cuda(device_id)
    def cpu(self):
        if not self.proposal_probabilities is None:
            self.proposal_probabilities = self.proposal_probabilities.cpu()

class Laplace(object):
    def __init__(self, prior_location, prior_scale):
        self.prior_location = prior_location
        self.prior_scale = prior_scale
        self.proposal_location = None
        self.proposal_scale = None

        self.name = 'Laplace'
        self.address_suffix = '_Laplace'
    def __repr__(self):
        return 'Laplace(prior_location:{0}, prior_scale:{1}, proposal_location:{2}, proposal_scale:{3})'.format(self.prior_location, self.prior_scale, self.proposal_location, self.proposal_scale)
    __str__ = __repr__
    def set_proposalparams(self, tensor_of_proposal_location_scale):
        self.proposal_location = tensor_of_proposal_location_scale[0]
        self.proposal_scale = tensor_of_proposal_location_scale[1]
    def cuda(self, device_id=None):
        return
    def cpu(self):
        return

class Gamma(object):
    def __init__(self):
        self.proposal_location = None
        self.proposal_scale = None

        self.name = 'Gamma'
        self.address_suffix = '_Gamma'
    def __repr__(self):
        return 'Gamma(proposal_location:{0}, proposal_scale:{1})'.format(self.proposal_location, self.proposal_scale)
    __str__ = __repr__
    def set_proposalparams(self, tensor_of_proposal_location_scale):
        self.proposal_location = tensor_of_proposal_location_scale[0]
        self.proposal_scale = tensor_of_proposal_location_scale[1]
    def cuda(self, device_id=None):
        return
    def cpu(self):
        return

class Beta(object):
    def __init__(self):
        self.proposal_mode = None
        self.proposal_certainty = None

        self.name = 'Beta'
        self.address_suffix = '_Beta'
    def __repr__(self):
        return 'Beta(proposal_mode:{0}, proposal_certainty:{1})'.format(self.proposal_mode, self.proposal_certainty)
    __str__ = __repr__
    def set_proposalparams(self, tensor_of_proposal_mode_certainty):
        self.proposal_mode = tensor_of_proposal_mode_certainty[0]
        self.proposal_certainty = tensor_of_proposal_mode_certainty[1]
    def cuda(self, device_id=None):
        return
    def cpu(self):
        return
