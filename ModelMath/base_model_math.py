from Indicators.indicator_listener import IndicatorListener
from MarketAdapter.security_market_view import SecurityMarketViewOnReadyListener
from abc import ABCMeta
from abc import abstractmethod

# Anyone who wishes to listen to ModelMath must extend this class
class ModelMathListener():
	__metaclass__ = ABCMeta
	
	@abstractmethod
	def UpdateTarget(self, _new_target_, _new_sum_vars_):
		return

class BaseModelMath(IndicatorListener, SecurityMarketViewOnReadyListener):
	__metaclass__ = ABCMeta
	
	def __init__(self, _watch_, _model_filename_):
		self.watch_ = _watch_
		self.model_filename_ = _model_filename_
		self.is_ready_vec_ = []
		self.readiness_required_vec_ = []
		self.is_ready_ = False
		self.last_is_ready_ = False
		self.model_stdev_ = 1.00 # Check whether it is needed
		self.model_math_listener_vec_ = [] # What is this
		self.indicator_vec_ = []
		self.prev_value_vec_ = []

	def GetModelFileName(self):
		return self.model_filename_
	
	def AddIndicator(self, _indicator_, _weight_, _readiness_required_):
		_indicator_.AddIndicatorListener(len(self.indicator_vec_), self, _weight_) # Why?
		self.indicator_vec_.append(_indicator_)
		self.prev_value_vec_.append(0)
		if (_indicator_.IsIndicatorReady()):
			self.is_ready_vec_.append(True)
			self.readiness_required_vec_.append(False)
		else:
			self.is_ready_vec_.append(False)
			self.readiness_required_vec_.append(_readiness_required_)
			self.is_ready_ = False

	def AddListener(self, _model_math_listener_):
		self.model_math_listener_vec_.append(_model_math_listener_)
		
	def PropagateNewTargetPrice(self, _new_target_, _new_sum_vars_):
		print('Propagating')
		#print('BaseModelMath.PropagateNewTargetPrice')
		#print(self.model_math_listener_vec_)
		for i in range(0, len(self.model_math_listener_vec_)):
			self.model_math_listener_vec_[i].UpdateTarget(_new_target_, _new_sum_vars_)
			
	def PropagateNotReady(self):
		for i in range(0, len(self.model_math_listener_vec_)):
			self.model_math_listener_vec_[i].TargetNotReady()
			
	@abstractmethod
	def SMVOnReady(self):
		return